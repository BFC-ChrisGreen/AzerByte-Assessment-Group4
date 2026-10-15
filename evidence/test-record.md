# Azerbyte Test Record

| Test | Expected result | Actual result | Pass/Fail | Completed by | Commit or evidence |
|---|---|---|---|---|---|
| API health check | Client receives an `online` JSON status | Client recieves the message "online" when the server is running, Client also recieves the message "the azerbyte service could not be reached" when the server is offline | Pass | Chris and Oday |  |
| Request /characters | Status 200 and a JSON list | worked | Pass | Chris
 |  |
|Request an existing character ID | Status 200 and one character| worked | Pass | Chris
|Request character ID 999 | Status 404 and a clear JSON error| worked | Pass | Chris
|Run the client with the server stopped | A clear connection message rather than a crash| worked | Pass | Chris