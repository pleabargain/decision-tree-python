# Decision Path Analysis

Generated from: `food_safety.txt`  
Date: 2025-03-22 11:58:06

## Decision Path Tree

```
└── Do you have a food thermometer available for temperature checks?
└── Yes
    └── Is the food stored at the proper temperature (below 40°F for refrigerated items, below 0°F for frozen items)?
    └── Yes
        └── Has the food been cooked to the appropriate internal temperature?
        └── Not sure
            └── Can you check the internal temperature with a food thermometer?
            └── Yes, and it's at proper temperature
                └── Are there any visible signs of spoilage (unusual color, texture, or odor)?
                └── Yes
                    └── RESULT: The food is UNSAFE. Visible signs of spoilage indicate bacterial growth, mold, or other decomposition that could cause foodborne illness. Never taste food to determine if it's safe.
```

## Visual Diagram

```mermaid
graph TD
    node_Q0["Do you have a food thermometer available for temperature checks?"]
    node_Q1["Is the food stored at the proper temperature (below 40°F for refrigerated items, below 0°F for frozen items)?"]
    node_Q2["Has the food been cooked to the appropriate internal temperature?"]
    node_Q2a["Can you check the internal temperature with a food thermometer?"]
    node_Q3["Are there any visible signs of spoilage (unusual color, texture, or odor)?"]
    node_R3["RESULT: The food is UNSAFE. Visible signs of spoilage indicate bacterial growth, mold, or other decomposition that could cause foodborne illness. Never taste food to determine if it's safe."]
    node_Q0 -->|"Yes"| node_Q1
    node_Q1 -->|"Yes"| node_Q2
    node_Q2 -->|"Not sure"| node_Q2a
    node_Q2a -->|"Yes, and it's at proper temperature"| node_Q3
    node_Q3 -->|"Yes"| node_R3

    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;
    classDef current fill:#d4f4ff,stroke:#0077b6,stroke-width:2px;
    classDef result fill:#d8f3dc,stroke:#2d6a4f,stroke-width:2px;
    class node_Q0,node_Q1,node_Q2,node_Q2a,node_Q3,node_R3 current;
    class node_R3 result;
```
