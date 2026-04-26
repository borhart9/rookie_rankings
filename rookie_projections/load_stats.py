# import nfl_data_py as nfl
import nflreadpy as nfl
import polars as pl
import duckdb

seasons = [2020, 2021, 2022, 2023, 2024, 2025]

stats = nfl.load_player_stats(seasons=seasons)
players = nfl.load_players()


result = duckdb.query("""
    with aggregated as (
    select 
        player_id, player_display_name as player, season, max(position) as position, count(distinct week) as games_played, sum(receptions) as receptions, sum(targets) as targets, sum(receiving_yards) as receiving_yards, 
                    sum(receiving_tds) as receiving_tds, sum(fantasy_points) as fantasy_points, sum(fantasy_points_ppr) as fantasy_points_ppr
    from
        stats
    where 
        position = 'WR'
        and season_type = 'REG'
    group by 
        player, player_id, season
    ),
    players as (
        select 
            gsis_id, college_name, rookie_season, draft_year, draft_round, draft_pick
        from 
            players
    )
    select 
        *
    from (
        select
            *
        from (
            select 
                a.* exclude (player_id),
                round(a.fantasy_points/a.games_played, 2) as FPPG,
                round(a.fantasy_points_ppr/a.games_played, 2) as FPPG_PPR,
                rank() over (
                    partition by a.season
                    order by (a.fantasy_points_ppr/a.games_played) desc
                        ) as season_rank,
                p.rookie_season,
                case 
                    when (a.season - p.rookie_season) = 0 then 'Rookie'
                    else cast((a.season - p.rookie_season) as string)
                END as year_in_league
            from
                aggregated a
                left join players p
                    on a.player_id = p.gsis_id
            where
                a.games_played >= 8
            qualify 
                season_rank <= 24
            order by 
                FPPG_PPR desc) temp
        where
            temp.year_in_league = '1' or temp.year_in_league = 'Rookie') temp2
    where
        (season = 2021 and year_in_league = 'Rookie')
        or (season = 2022)
        or (season = 2023 and year_in_league = '1')
        or (season = 2024 and year_in_league = 'Rookie')
        or (season = 2025 and year_in_league = '1')
""").pl()


pl.Config.set_tbl_cols(-1)
pl.Config.set_tbl_rows(-1)
print(result)

result.write_csv("rookie_projections\\stats.csv")