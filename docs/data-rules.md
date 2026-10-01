# Azerbyte Data Rules

Record the final agreed names, data types, required fields and validation rules used by every component.

| Field | Data type | Required? | Rules | Example |
|---|---|---|---|---|
| `character_id` | Integer | Yes | Unique positive value | `1` |
| `name` | String | Yes | To be agreed by the group | `Aelwyn` |
| `character_class` | String | Yes | To be agreed by the group | `Mage` |
| `level` | Integer | Yes | To be agreed by the group | `12` |
| `realm` | String | Yes | To be agreed by the group | `Emberfall` |

## Synchronisation and Consistency Notes

Record situations where different clients could access or update the same data and how the prototype handles them.

