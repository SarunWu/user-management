## Know issues log
### GET /migrate/tables/overview/all
- Can't do concurrent because it isn't allowed to open new connection with this approach
```
results = await asyncio.gather(user.summarize(db_session),
                               user_group.summarize(db_session),
                               feature.summarize(db_session),
                               migrate_status.summarize(db_session))
```
