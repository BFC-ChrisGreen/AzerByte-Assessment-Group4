# Azerbyte Test Record

| Test | Expected result | Actual result | Pass/Fail | Completed by | Commit or evidence |
|---|---|---|---|---|---|
| API health check | Client receives an `online` JSON status | Client recieves the message "online" when the server is running, Client also recieves the message "the azerbyte service could not be reached" when the server is offline | Pass | Chris and Oday |  |
| Request /characters | Status 200 and a JSON list | worked | Pass | Chris
 |  |
|Request an existing character ID | Status 200 and one character| worked | Pass | Chris
|Request character ID 999 | Status 404 and a clear JSON error| worked | Pass | Chris
|Run the client with the server stopped | A clear connection message rather than a crash| worked | Pass | Chris 
|Run the database setup twice | Both runs complete and only two starter records exist | worked | pass | Bailey and Oday 
|Request /characters | Status 200 and two database records | worked | pass | Bailey and Oday
|Request /characters/1 | Status 200 and Aelwyn's record | worked | pass | Bailey and Oday
|Request /characters/999 | Status 404 and Character not found | worked | pass | Bailey and Oday
|Restart Flask and request the characters again | The same records are still returned | worked | pass | Bailey and Oday
|Run setup on another group member's clone | Their local database is created successfully | worked | pass | Bailey and Oday
 Test | Expected result | Actual result | Pass/Fail | Completed by | Commit or evidence |
|View all characters|Every stored character is displayed|as expected|pass|oday|| 
Find existing character|Status 404 and a clear error|as expected|pass|oday||
Find missing character|Status 404 and a clear error|as expected|pass|oday||
Create valid character|Status 201 and a generated ID|as expected|pass|oday||
Create level 99|Status 400 and a validation error|as expected|pass|oday||
Update existing character|Status 200 and the changed record|as expected|pass|oday||
Update ID 999|Status 404 and a clear error|as expected|pass|oday||
Restart Flask and find the new character|Created and updated values remain|as expected|pass|oday||
Stop Flask and run the client|A clear unavailable-service message|as expected|pass|oday||
