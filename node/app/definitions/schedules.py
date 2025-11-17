import dagster as dg

from app.definitions import jobs

hourly_wine_quality_asset_schedule = dg.ScheduleDefinition(
    job=jobs.hourly_wine_quality_asset_job,
    cron_schedule="0 * * * *"
)


asset_schedules = [
    hourly_wine_quality_asset_schedule,
]
