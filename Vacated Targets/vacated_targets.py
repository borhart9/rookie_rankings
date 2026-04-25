import nflreadpy as nfl
import polars as pl
import duckdb

stats_seasons = [2020, 2021, 2022, 2023, 2024]
rosters_season = [2021, 2022, 2023, 2024, 2025]

stats = nfl.load_player_stats(seasons=stats_seasons)
rosters = nfl.load_rosters_weekly(seasons=rosters_season)

results = duckdb.query("""
    with player_targets as (
    select
        player_display_name as player, player_id, team, sum(targets) as targets, position, season
    from 
        stats
    where 
        position in ('WR', 'TE', 'RB')
        and season_type = 'REG'
        and targets > 0
    group by
        team, position, player, player_id, season
    order by 
        targets desc
    ),
    position_targets as (
        select
            team, sum(targets) as targets, position, season
        from
            stats
        where 
            season_type = 'REG'
        group by
            team, position, season
        order by 
            targets desc
    ),
    team_targets as (
        select
            team, sum(targets) as targets, season
        from
            stats
        where 
            season_type = 'REG'
        group by 
            team, season
        order by 
            targets desc
    )
    select
        pt.player,
        pt.team,
        pt.player_id,
        pt.position,
        pt.season,
        pt.targets as player_targets,
        post.targets as position_targets,
        tt.targets as team_targets,
        round((pt.targets/post.targets), 2) as position_target_share,
        round((pt.targets/tt.targets), 2) as team_target_share
    from
        player_targets pt
        left join position_targets post
            on pt.team = post.team
            and pt.position = post.position
            and pt.season = post.season
        left join team_targets tt
            on pt.team = tt.team
            and pt.season = tt.season
    order by 
        player_targets desc
    """)

on_roster = duckdb.query("""
    select
        full_name as player, gsis_id as player_id, status, team, week, season
    from
        rosters
    where 
        week = 1
        and position in ('WR', 'TE', 'RB')
""")

position_vacated_targets = duckdb.query("""
    with aggregated as (select 
        r.player, r.player_id, r.player_targets, r.team, r.position, rst.team, (r.season + 1) as season
    from
        results r
        left join on_roster rst
            on r.player_id = rst.player_id
            and r.season = (rst.season - 1)
    where
        rst.team is null
        or rst.team != r.team                              
    order by 
        r.player_targets desc
    )
    select  
        sum(player_targets) as vacated_targets, team, position
    from
        aggregated a
    group by 
        team, position, season
    order by 
        vacated_targets desc
""")

team_vacated_targets = duckdb.query("""
    with aggregated as (
        select 
            r.player, r.player_id, r.player_targets, r.team_targets, r.position_targets, 
                r.team, r.position, rst.team, (r.season + 1) as season
    from
        results r
        left join on_roster rst
            on r.player_id = rst.player_id
            and r.season = (rst.season - 1)
    where
        rst.team is null
        or rst.team != r.team                              
    order by 
        r.player_targets desc
    )
    select  
        sum(player_targets) as vacated_targets, max(team_targets) as team_targets, 
            max(position_targets) as position_targets, team, season, position
    from
        aggregated a
    group by 
        team, season, position
    order by 
        vacated_targets desc
""")

pl.Config.set_tbl_cols(-1)
pl.Config.set_tbl_rows(-1)

