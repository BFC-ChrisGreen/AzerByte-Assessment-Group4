# Azerbyte Data Rules

Record the final agreed names, data types, required fields and validation rules used by every component.

| Field | Data type | Required? | Rules | Example |
|---|---|---|---|---|
| `character_id` | Integer | Yes | Unique positive value  | `1` |
| `name` | String | Yes | Between 2 and 30 characters  | `Aelwyn` |
| `character_class` | String | Yes | 	Warrior, Mage, Rogue, Priest or Ranger | `Mage` |
| `level` | Integer | Yes | Between 1 and 60| `12` |
| `realm` | String | Yes | Orgrimmar, Stormwatch, Winterspring, Hinterlands | `orgrimmar` |

## Synchronisation and Consistency Notes

Record situations where different clients could access or update the same data and how the prototype handles them.

