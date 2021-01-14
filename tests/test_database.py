import pytest


@pytest.mark.parametrize(
    "item, expected",
    (
        (
            "routines",
            {
                "lastdateofmonth",
                "season",
                "daily_ts",
                "monthly_ts",
                "query_one_station",
                "query_one_station_climo",
                "do_query_one_station",
                "daysinmonth",
                "getstationvariabletable",
                "updatesdateedate",
                "effective_day",
                "closest_stns_within_threshold",
            },
        ),
        (
            "tables",
            {"meta_network", 'meta_contact', 'meta_station', 'meta_history'},
        ),
        (
            "views",
            {
                'crmp_network_geoserver',
                'history_join_station_network',
                'obs_count_per_day_history_v',
                'obs_with_flags',
            },
        ),
    ),
)
def test_database_migration(
    pycds_engine,
    schema_name,
    get_schema_item_names,
    item,
    expected
):
    result = get_schema_item_names(pycds_engine, item, schema_name)
    # print(f"{item}:", result)
    assert result >= expected
