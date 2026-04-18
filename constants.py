"""
Section/field metadata for rwGUI.
Python translation of constants.ts — all fixes applied:
  - No dead types (ModData removed)
  - isMulti flag explicit on every section
"""

SECTIONS_DATA = {
    "modInfoSection": {
        "id": "mod_info",
        "title": "Mod Manifest",
        "description": "Configuration for mod-info.txt used by the game browser.",
        "isMulti": False,
        "fields": [
            {"id": "title",               "label": "Mod Title",          "type": "string",  "description": "Display name of the mod.",                    "example": "My Awesome Mod"},
            {"id": "description",         "label": "Description",        "type": "string",  "description": "Brief overview of what the mod does.",         "example": "Adds new experimental units."},
            {"id": "id",                  "label": "Internal ID",        "type": "string",  "description": "Unique ID for dependency tracking.",           "example": "com.user.coolmod"},
            {"id": "tags",                "label": "Tags",               "type": "string",  "description": "Comma-separated tags (e.g. units, sample).",   "example": "units, tank"},
            {"id": "minVersion",          "label": "Min Version",        "type": "string",  "description": "Minimum game version required.",               "example": "1.15"},
            {"id": "requiredMods",        "label": "Required Mods",      "type": "string",  "description": "List of mod IDs this depends on.",             "example": "base-expansion"},
            {"id": "requiredModsMessage", "label": "Missing Dep Message","type": "string",  "description": "Message shown if dependencies are missing.",   "example": "Please install the Base Expansion mod."},
        ],
    },

    "modSections": [
        {
            "id": "core", "title": "Core Unit Functions", "isMulti": False,
            "description": "Basic unit characteristics: HP, price, mass, radius.",
            "fields": [
                {"id": "name",                "label": "Unit Name",       "type": "string",  "description": "Internal unit name for identification.",      "example": "customTank1"},
                {"id": "maxHp",               "label": "Max HP",          "type": "number",  "description": "Maximum health points.",                      "example": "200"},
                {"id": "price",               "label": "Price",           "type": "price",   "description": "Cost to build (credits, resources).",         "example": "500, gold=10"},
                {"id": "mass",                "label": "Mass",            "type": "number",  "description": "Weight — affects collisions.",                "example": "3000"},
                {"id": "radius",              "label": "Selection Radius","type": "number",  "description": "Circular area for selection/collision.",       "example": "20"},
                {"id": "techLevel",           "label": "Tech Level",      "type": "enum",    "description": "Tech tier of the unit.",                      "example": "1",   "options": ["1","2","3"]},
                {"id": "buildSpeed",          "label": "Build Speed",     "type": "string",  "description": "Time to build (e.g. 3s or 0.01).",            "example": "3s"},
                {"id": "isBio",               "label": "Is Biological?",  "type": "boolean", "description": "Affects sounds and splats.",                  "example": "false"},
                {"id": "isBuilder",           "label": "Is Builder?",     "type": "boolean", "description": "Required for placing buildings.",             "example": "false"},
                {"id": "soundOnAttackOrder",  "label": "Attack Sound",    "type": "sound",   "description": "Played when ordered to attack.",              "example": "tankAttack.wav"},
                {"id": "soundOnMoveOrder",    "label": "Move Sound",      "type": "sound",   "description": "Played when ordered to move.",                "example": "tankMove.wav"},
                {"id": "soundOnNewSelection", "label": "Select Sound",    "type": "sound",   "description": "Played when unit is selected.",               "example": "tankSelect.wav"},
                {"id": "soundOnDeath",        "label": "Death Sound",     "type": "sound",   "description": "Played when unit is destroyed.",              "example": "explosion.wav"},
            ],
        },
        {
            "id": "graphics", "title": "Graphics & Visuals", "isMulti": False,
            "description": "Body sprites, shadows, draw layers.",
            "fields": [
                {"id": "image",            "label": "Body Image",    "type": "file",   "description": "Path to unit body sprite.",           "example": "body.png"},
                {"id": "total_frames",     "label": "Total Frames",  "type": "number", "description": "Number of frames for body animation.","example": "1"},
                {"id": "image_wreak",      "label": "Wreck Image",   "type": "file",   "description": "Image used when unit dies.",          "example": "wreck.png"},
                {"id": "imageScale",       "label": "Image Scale",   "type": "float",  "description": "Multiplier for image size.",          "example": "1.0"},
                {"id": "drawLayer",        "label": "Draw Layer",    "type": "enum",   "description": "Rendering priority.",                 "example": "ground",    "options": ["ground","ground2","air","top","underwater"]},
                {"id": "teamColoringMode", "label": "Team Coloring", "type": "enum",   "description": "Pixel treatment for team colours.",   "example": "pureGreen", "options": ["pureGreen","hueAdd","hueShift","disabled"]},
            ],
        },
        {
            "id": "attack", "title": "Attack Permissions", "isMulti": False,
            "description": "Global characteristics for targeting enemies.",
            "fields": [
                {"id": "canAttack",                 "label": "Can Attack?",    "type": "boolean", "description": "Allow or disallow all attacks.",         "example": "true"},
                {"id": "canAttackFlyingUnits",       "label": "Attack Air?",   "type": "boolean", "description": "Target flying units.",                   "example": "true"},
                {"id": "canAttackLandUnits",         "label": "Attack Land?",  "type": "boolean", "description": "Target ground units.",                   "example": "true"},
                {"id": "canAttackUnderwaterUnits",   "label": "Attack Water?", "type": "boolean", "description": "Target underwater units.",               "example": "false"},
                {"id": "maxAttackRange",             "label": "Max Range",     "type": "number",  "description": "Maximum targeting distance.",            "example": "250"},
                {"id": "shootDelay",                 "label": "Shoot Delay",   "type": "string",  "description": "Interval between shots (ticks).",        "example": "50"},
            ],
        },
        {
            "id": "movement", "title": "Movement", "isMulti": False,
            "description": "Speed, acceleration, and terrain types.",
            "fields": [
                {"id": "movementType",          "label": "Movement Type", "type": "enum",  "description": "Terrain compatibility.",         "example": "LAND", "options": ["NONE","LAND","AIR","WATER","HOVER","BUILDING","OVER_CLIFF"]},
                {"id": "moveSpeed",             "label": "Move Speed",    "type": "float", "description": "Maximum movement velocity.",     "example": "1.2"},
                {"id": "moveAccelerationSpeed", "label": "Acceleration",  "type": "float", "description": "Speed increase per frame.",      "example": "0.07"},
                {"id": "maxTurnSpeed",          "label": "Turn Speed",    "type": "float", "description": "Top rotation speed.",            "example": "4.0"},
                {"id": "targetHeight",          "label": "Target Height", "type": "number","description": "Operating altitude.",            "example": "0"},
            ],
        },
        {
            "id": "ai", "title": "AI Behavior", "isMulti": False,
            "description": "How computer-controlled teams use this unit.",
            "fields": [
                {"id": "useAsBuilder",   "label": "Use as Builder?",   "type": "boolean","description": "AI uses this to build structures.", "example": "false"},
                {"id": "useAsTransport", "label": "Use as Transport?", "type": "boolean","description": "AI uses this to move units.",       "example": "true"},
                {"id": "buildPriority",  "label": "Build Priority",    "type": "float",  "description": "Likelihood of AI building (0-1).", "example": "0.8"},
                {"id": "maxGlobal",      "label": "Max Global Limit",  "type": "number", "description": "Max amount for AI per map.",       "example": "50"},
            ],
        },
    ],

    "multiSections": [
        {
            "id": "turret", "title": "Turret", "isMulti": True,
            "description": "Turrets fire projectiles with independent targeting.",
            "fields": [
                {"id": "id",              "label": "Turret ID",     "type": "string",  "description": "Unique name for this turret.",         "example": "gun1"},
                {"id": "x",              "label": "X Position",    "type": "number",  "description": "Horizontal offset from unit center.",  "example": "0"},
                {"id": "y",              "label": "Y Position",    "type": "number",  "description": "Vertical offset from unit center.",    "example": "0"},
                {"id": "projectile",     "label": "Projectile ID", "type": "string",  "description": "The projectile fired by this turret.", "example": "1"},
                {"id": "turnSpeed",      "label": "Turn Speed",    "type": "float",   "description": "Rotation speed.",                      "example": "2.0"},
                {"id": "shoot_sound",    "label": "Shoot Sound",   "type": "sound",   "description": "Sound played when firing.",            "example": "cannon_fire.wav"},
                {"id": "shoot_sound_vol","label": "Shoot Volume",  "type": "float",   "description": "Volume level (0-1).",                  "example": "0.5"},
                {"id": "canShoot",       "label": "Can Shoot?",    "type": "boolean", "description": "If false, used for visuals/build.",    "example": "true"},
                {"id": "invisible",      "label": "Is Invisible?", "type": "boolean", "description": "Hide the turret sprite.",              "example": "false"},
            ],
        },
        {
            "id": "projectile", "title": "Projectile", "isMulti": True,
            "description": "Defines damage and flight behaviour.",
            "fields": [
                {"id": "id",           "label": "Projectile ID", "type": "string", "description": "Unique identifier.",       "example": "1"},
                {"id": "directDamage", "label": "Direct Damage", "type": "number", "description": "Damage on hit.",            "example": "30"},
                {"id": "life",         "label": "Life (Ticks)",  "type": "number", "description": "Lifespan of projectile.", "example": "200"},
                {"id": "speed",        "label": "Speed",         "type": "float",  "description": "Flight velocity.",         "example": "5.0"},
                {"id": "image",        "label": "Image",         "type": "file",   "description": "Projectile sprite.",       "example": "bullet.png"},
                {"id": "areaDamage",   "label": "Area Damage",   "type": "number", "description": "Splash damage.",           "example": "0"},
                {"id": "areaRadius",   "label": "Area Radius",   "type": "number", "description": "Splash radius.",           "example": "0"},
            ],
        },
        {
            "id": "action", "title": "Action", "isMulti": True,
            "description": "Dynamic abilities triggered by players.",
            "fields": [
                {"id": "id",               "label": "Action ID",       "type": "string", "description": "Unique identifier.",                              "example": "repair"},
                {"id": "text",             "label": "Button Text",     "type": "string", "description": "Label on the UI button.",                        "example": "Repair Self"},
                {"id": "description",      "label": "Tool-tip",        "type": "string", "description": "Hover description.",                             "example": "Fix internal systems."},
                {"id": "price",            "label": "Price",           "type": "price",  "description": "Cost to trigger.",                               "example": "credits=500"},
                {"id": "playSoundAtUnit",  "label": "Unit Sound",      "type": "sound",  "description": "Sound played at the unit when action is used.",  "example": "repair.wav"},
                {"id": "playSoundGlobally","label": "Global Sound",    "type": "sound",  "description": "Sound played to everyone.",                      "example": "alert.wav"},
                {"id": "autoTrigger",      "label": "Auto Trigger",    "type": "logic",  "description": "LogicBoolean for auto-activation.",              "example": "if self.hp() < 100"},
                {"id": "convertTo",        "label": "Convert To",      "type": "string", "description": "Transform unit into another type.",              "example": "upgradedTank"},
            ],
        },
        {
            "id": "hiddenAction", "title": "Hidden Action", "isMulti": True,
            "description": "Actions triggered by logic without button visibility.",
            "fields": [
                {"id": "id",               "label": "Hidden Action ID","type": "string", "description": "Unique identifier.",                              "example": "autoRepair"},
                {"id": "autoTrigger",      "label": "Auto Trigger",    "type": "logic",  "description": "LogicBoolean for auto-activation.",              "example": "if self.hp() < 100"},
                {"id": "convertTo",        "label": "Convert To",      "type": "string", "description": "Transform unit into another type.",              "example": "upgradedTank"},
                {"id": "playSoundAtUnit",  "label": "Unit Sound",      "type": "sound",  "description": "Sound played at unit when triggered.",           "example": "repair.wav"},
            ],
        },
        {
            "id": "animation", "title": "Animation", "isMulti": True,
            "description": "Frame-by-frame movement for body, turrets, and legs.",
            "fields": [
                {"id": "id",        "label": "Animation ID",    "type": "string",  "description": "Name of the animation.",                             "example": "idle"},
                {"id": "onActions", "label": "Trigger On",      "type": "string",  "description": "When this plays (idle, move, attack, etc.).",        "example": "move, idle"},
                {"id": "blendIn",   "label": "Blend In (s)",    "type": "float",   "description": "Transition-in time.",                                "example": "0.1"},
                {"id": "blendOut",  "label": "Blend Out (s)",   "type": "float",   "description": "Transition-out time.",                               "example": "0.1"},
                {"id": "pingPong",  "label": "Ping-Pong?",      "type": "boolean", "description": "Reverse at end of loop.",                            "example": "true"},
                {"id": "Keyframes", "label": "Keyframes (Raw)", "type": "logic",   "description": "Time-based frame data (body_0s: {frame:0}).",        "example": "body_0s: {frame:0}\nbody_0.5s: {frame:4}"},
            ],
        },
        {
            "id": "canBuild", "title": "Build Menu", "isMulti": True,
            "description": "Units that this unit can build.",
            "fields": [
                {"id": "name",      "label": "Unit ID",      "type": "string",  "description": "Unit identifier to build.",       "example": "heavyTank"},
                {"id": "pos",       "label": "UI Position",  "type": "float",   "description": "Order in build menu.",            "example": "1.0"},
                {"id": "tech",      "label": "Tech Tier",    "type": "number",  "description": "Required tech level.",            "example": "1"},
                {"id": "forceNano", "label": "Force Nano?",  "type": "boolean", "description": "Build as if structure.",          "example": "false"},
                {"id": "isVisible", "label": "Is Visible?",  "type": "logic",   "description": "Condition to show button.",       "example": "if self.hp() > 50"},
                {"id": "isLocked",  "label": "Is Locked?",   "type": "logic",   "description": "Condition to disable button.",    "example": "if not self.energy() > 10"},
            ],
        },
        {
            "id": "leg", "title": "Leg / Arm", "isMulti": True,
            "description": "Moveable cosmetics for mechs, infantry, etc.",
            "fields": [
                {"id": "x",           "label": "X Foot Pos",   "type": "float", "description": "Foot position horizontal.",      "example": "10"},
                {"id": "y",           "label": "Y Foot Pos",   "type": "float", "description": "Foot position vertical.",        "example": "10"},
                {"id": "attach_x",    "label": "Attach X",     "type": "float", "description": "Joint point horizontal.",        "example": "5"},
                {"id": "attach_y",    "label": "Attach Y",     "type": "float", "description": "Joint point vertical.",          "example": "5"},
                {"id": "rotateSpeed", "label": "Rotate Speed", "type": "float", "description": "Leg rotation velocity.",         "example": "2.0"},
                {"id": "heightSpeed", "label": "Height Speed", "type": "float", "description": "Vertical movement velocity.",    "example": "1.0"},
                {"id": "moveSpeed",   "label": "Move Speed",   "type": "float", "description": "Walking speed.",                 "example": "2.5"},
                {"id": "image_leg",   "label": "Leg Image",    "type": "file",  "description": "Leg sprite asset.",              "example": "leg.png"},
                {"id": "image_foot",  "label": "Foot Image",   "type": "file",  "description": "Foot sprite asset.",             "example": "foot.png"},
            ],
        },
        {
            "id": "arm", "title": "Arm", "isMulti": True,
            "description": "Alternative numbered limb section (`arm_`) from reference sheet.",
            "fields": [
                {"id": "x",           "label": "X Pos",       "type": "float", "description": "Arm position horizontal.",          "example": "10"},
                {"id": "y",           "label": "Y Pos",       "type": "float", "description": "Arm position vertical.",            "example": "10"},
                {"id": "attach_x",    "label": "Attach X",    "type": "float", "description": "Joint point horizontal.",           "example": "5"},
                {"id": "attach_y",    "label": "Attach Y",    "type": "float", "description": "Joint point vertical.",             "example": "5"},
                {"id": "rotateSpeed", "label": "Rotate Speed","type": "float", "description": "Rotation velocity.",                 "example": "2.0"},
                {"id": "image_end",   "label": "End Image",   "type": "file",  "description": "Sprite for arm ending.",            "example": "arm_end.png"},
            ],
        },
        {
            "id": "attachment", "title": "Attachment", "isMulti": True,
            "description": "Units stacked onto this one to create compound units.",
            "fields": [
                {"id": "id",                          "label": "Slot ID",        "type": "string",  "description": "Name of attachment slot.",          "example": "cannon_mount"},
                {"id": "x",                           "label": "X Position",     "type": "float",   "description": "Horizontal offset.",                "example": "0"},
                {"id": "y",                           "label": "Y Position",     "type": "float",   "description": "Vertical offset.",                  "example": "10"},
                {"id": "height",                      "label": "Height",         "type": "float",   "description": "Elevation offset.",                 "example": "5"},
                {"id": "idleDir",                     "label": "Idle Dir",       "type": "number",  "description": "Facing direction (degrees).",       "example": "0"},
                {"id": "isVisible",                   "label": "Is Visible?",    "type": "boolean", "description": "Show the attachment.",              "example": "true"},
                {"id": "canAttack",                   "label": "Can Attack?",    "type": "boolean", "description": "Attachment can fire.",              "example": "true"},
                {"id": "onCreateSpawnUnitOf",          "label": "Unit Type",      "type": "string",  "description": "Unit to spawn in slot.",            "example": "smallTurret"},
                {"id": "prioritizeParentsMainTarget", "label": "Share Target?",  "type": "boolean", "description": "Target parent's enemy.",            "example": "true"},
            ],
        },
        {
            "id": "effect", "title": "Effect", "isMulti": True,
            "description": "Visual effects spawned by the unit.",
            "fields": [
                {"id": "id",            "label": "Effect ID",   "type": "string", "description": "Unique name.",              "example": "smoke"},
                {"id": "life",          "label": "Lifespan",    "type": "float",  "description": "Time till removal (ticks).","example": "100"},
                {"id": "image",         "label": "Image",       "type": "file",   "description": "Sprite asset.",             "example": "puff.png"},
                {"id": "scaleTo",       "label": "Scale To",    "type": "float",  "description": "End scale.",                "example": "2.0"},
                {"id": "scaleFrom",     "label": "Scale From",  "type": "float",  "description": "Start scale.",              "example": "1.0"},
                {"id": "color",         "label": "Tint Color",  "type": "string", "description": "Hex colour code.",          "example": "#FFFFFF"},
                {"id": "fadeInTime",    "label": "Fade In (s)", "type": "float",  "description": "Alpha transition time.",    "example": "0.2"},
                {"id": "xSpeedRelative","label": "Speed X",     "type": "float",  "description": "Horizontal drift.",         "example": "0.5"},
                {"id": "ySpeedRelative","label": "Speed Y",     "type": "float",  "description": "Vertical drift.",           "example": "0.5"},
            ],
        },
        {
            "id": "placementRule", "title": "Placement Rule", "isMulti": True,
            "description": "Rules for where buildings can be placed.",
            "fields": [
                {"id": "id",                  "label": "Rule ID",       "type": "string", "description": "Unique name.",                   "example": "nearFactory"},
                {"id": "searchTags",          "label": "Search Tags",   "type": "string", "description": "Find units with these tags.",    "example": "factory"},
                {"id": "searchTeam",          "label": "Search Team",   "type": "enum",   "description": "Who to look for.",               "example": "own", "options": ["own","neutral","ally","enemy","any"]},
                {"id": "searchDistance",      "label": "Distance",      "type": "number", "description": "Radius to check.",               "example": "500"},
                {"id": "minCount",            "label": "Min Units",     "type": "number", "description": "Required minimum.",              "example": "1"},
                {"id": "maxCount",            "label": "Max Units",     "type": "number", "description": "Required maximum.",              "example": "10"},
                {"id": "cannotPlaceMessage",  "label": "Error Message", "type": "string", "description": "Shown if placement failed.",     "example": "Requires a factory nearby."},
            ],
        },
        {
            "id": "globalResource", "title": "Global Resource", "isMulti": True,
            "description": "Team-level resource shared globally in matches.",
            "fields": [
                {"id": "id",               "label": "Resource ID",   "type": "string",  "description": "Internal name.",                "example": "metal"},
                {"id": "displayName",      "label": "Display Name",  "type": "string",  "description": "Visible name.",                 "example": "Metal"},
                {"id": "displayNameShort", "label": "Short Name",    "type": "string",  "description": "Compact label.",                "example": "Met"},
                {"id": "hidden",           "label": "Is Hidden?",    "type": "boolean", "description": "Hide from player UI.",          "example": "false"},
            ],
        },
        {
            "id": "resource", "title": "Local Resource", "isMulti": True,
            "description": "Local resource used by units (e.g. ammo, fuel).",
            "fields": [
                {"id": "id",               "label": "Resource ID",   "type": "string",  "description": "Internal name.",       "example": "ammo"},
                {"id": "displayName",      "label": "Display Name",  "type": "string",  "description": "Visible name.",        "example": "Missiles"},
                {"id": "displayNameShort", "label": "Short Name",    "type": "string",  "description": "Compact label.",       "example": "Msl"},
                {"id": "hidden",           "label": "Is Hidden?",    "type": "boolean", "description": "Hide from player UI.", "example": "false"},
            ],
        },
        {
            "id": "decal", "title": "Decal", "isMulti": True,
            "description": "Graphics layered onto the unit body.",
            "fields": [
                {"id": "image",           "label": "Decal Image", "type": "file",   "description": "Sprite asset.",              "example": "logo.png"},
                {"id": "layer",           "label": "Layer",       "type": "enum",   "description": "Stacking priority.",          "example": "onTop", "options": ["shadow","beforeBody","afterBody","onTop","beforeUI"]},
                {"id": "order",           "label": "Sort Order",  "type": "float",  "description": "Sub-layer priority.",         "example": "1.0"},
                {"id": "xOffsetRelative", "label": "X Offset",    "type": "float",  "description": "Horizontal shift.",           "example": "0"},
                {"id": "yOffsetRelative", "label": "Y Offset",    "type": "float",  "description": "Vertical shift.",             "example": "0"},
                {"id": "isVisible",       "label": "Is Visible?", "type": "logic",  "description": "Condition to draw.",          "example": "if self.hp() > 0"},
            ],
        },
        {
            "id": "comment", "title": "Comment", "isMulti": True,
            "description": "Note-only section for documentation (`comment_NAME`).",
            "fields": [
                {"id": "id",      "label": "Comment ID", "type": "string", "description": "Unique comment section name.", "example": "todoBalance"},
                {"id": "text",    "label": "Comment",    "type": "string", "description": "Free text note.",               "example": "Increase hp if too weak."},
            ],
        },
        {
            "id": "template", "title": "Template Section", "isMulti": True,
            "description": "Reusable template section (`template_NAME`) referenced by units.",
            "fields": [
                {"id": "id",   "label": "Template ID", "type": "string", "description": "Template section name.",     "example": "infantryBase"},
                {"id": "text", "label": "Template Raw","type": "logic",  "description": "Raw fields for template use.", "example": "maxHp:120\nmass:40"},
            ],
        },
    ],
}
