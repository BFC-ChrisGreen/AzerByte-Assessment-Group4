# Azerbyte Technical Decisions

Use this document to record important decisions as the prototype develops.

| Decision | Chosen approach | Alternatives considered | Reason | Date |
|---|---|---|---|---|
| Client-to-server communication | HTTP with JSON |  |  |  |
| Server middleware | Flask | Nothing | Flask allows for middleware with request hooks, this allows for user friendly data store and editing data through requests. | 06/11/2026 |
| Persistent storage | SQLite | Nothing | SQL Lite was chosen over other alternatives due to the minimal configuration with low maintenance allowing for a easier user experience managing the database. It is also suited for light workloads and data store which is best fit for AzerByte. | 06/11/2026 |
| Client Communication moved to API_Client | API_Client | It allows for different proccesses to be achived, by providing errors codes for problem. | 12/11/2026 |