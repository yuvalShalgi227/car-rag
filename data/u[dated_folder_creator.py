import os
from pathlib import Path
import json


def write_readme(path: Path, text: str):
    (path / "README.txt").write_text(text, encoding="utf-8")


def create_kb_structure(base_path: str):
    base = Path(base_path)

    # Top-level folders and explanations
    folders = {
        "manuals": (
            "This folder stores full car manuals.\n"
            "Structure: manufacturer → model → year.\n"
            "Each file is a complete manual (PDF) used for deep technical answers."
        ),
        "specs": (
            "This folder contains structured technical specifications.\n"
            "Structure: manufacturer → model.\n"
            "Files should be JSON with key vehicle specifications such as oil type, capacities, and pressures."
        ),
        "manufacturers": (
            "This folder stores manufacturer-level information.\n"
            "Includes brand-wide notes, known issues, and metadata shared across all models."
        ),
        "warnings": (
            "This folder contains the complete catalog of vehicle warning lights.\n"
            "Includes a JSON file with structured definitions and a subfolder for reference icon images.\n"
            "Used by the RAG system to match detected symbols with known warning lights."
        )
    }

    # Example subfolders
    examples = {
        "manuals": ["Toyota/Corolla/2018", "Mazda/3/2016"],
        "specs": ["Toyota/Corolla", "Mazda/3"],
        "manufacturers": ["Toyota", "Mazda"],
        "warnings": ["warning_lights_images"]
    }

    # Create folders + README files
    for folder, description in folders.items():
        folder_path = base / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        write_readme(folder_path, description)

        for sub in examples[folder]:
            sub_path = folder_path / sub
            sub_path.mkdir(parents=True, exist_ok=True)

            write_readme(
                sub_path,
                (
                    f"This is an example subfolder for the '{folder}' category.\n"
                    f"Path: {sub_path}\n\n"
                    "Place real files here according to this structure.\n"
                    "LLM Note: Files must contain domain-consistent information for accurate RAG responses."
                )
            )

    # --- Full English warning lights dataset ---
    warning_lights = [
        {
            "id": "oil_pressure",
            "keywords": ["oil", "oil pressure", "engine oil"],
            "name_en": "Low Oil Pressure",
            "severity_level": 5,
            "urgency_level": 5,
            "drive_restriction": "Do not continue driving",
            "description_en": "Engine oil pressure is critically low. Continuing to drive may cause severe engine damage.",
            "action_en": "Stop immediately, turn off the engine, and check the oil level. If the issue persists, call for towing."
        },
        {
            "id": "engine_overheat",
            "keywords": ["engine hot", "coolant temperature", "high temperature"],
            "name_en": "Engine Overheating",
            "severity_level": 5,
            "urgency_level": 5,
            "drive_restriction": "Do not drive",
            "description_en": "The engine temperature is dangerously high.",
            "action_en": "Stop immediately, shut off the engine, allow it to cool, and check coolant level."
        },
        {
            "id": "battery_charge",
            "keywords": ["battery", "charging system"],
            "name_en": "Charging System Fault",
            "severity_level": 4,
            "urgency_level": 3,
            "drive_restriction": "Short driving allowed only",
            "description_en": "The battery is not being charged.",
            "action_en": "Drive only short distances and visit a workshop soon."
        },
        {
            "id": "brake_system",
            "keywords": ["brake", "brake fault"],
            "name_en": "Brake System Fault",
            "severity_level": 5,
            "urgency_level": 5,
            "drive_restriction": "Do not continue driving",
            "description_en": "Critical brake system issue.",
            "action_en": "Stop immediately and arrange towing."
        },
        {
            "id": "steering_failure",
            "keywords": ["steering", "power steering"],
            "name_en": "Power Steering Failure",
            "severity_level": 4,
            "urgency_level": 4,
            "drive_restriction": "Drive very carefully",
            "description_en": "Power steering assistance is reduced or disabled.",
            "action_en": "Drive slowly and visit a workshop."
        },
        {
            "id": "airbag_srs",
            "keywords": ["airbag", "srs"],
            "name_en": "Airbag / SRS Fault",
            "severity_level": 4,
            "urgency_level": 3,
            "drive_restriction": "Driving allowed but unsafe",
            "description_en": "The airbag system may not function during a collision.",
            "action_en": "Have the system inspected soon."
        },
        {
            "id": "check_engine",
            "keywords": ["engine", "check engine"],
            "name_en": "Check Engine",
            "severity_level": 3,
            "urgency_level": 2,
            "drive_restriction": "Driving allowed with caution",
            "description_en": "General engine or emissions system fault.",
            "action_en": "Have the vehicle inspected soon. If the light flashes, stop driving."
        },
        {
            "id": "tpms",
            "keywords": ["tire pressure", "tpms"],
            "name_en": "Low Tire Pressure",
            "severity_level": 2,
            "urgency_level": 2,
            "drive_restriction": "Driving allowed with caution",
            "description_en": "One or more tires have low pressure.",
            "action_en": "Inflate the tires to proper pressure."
        },
        {
            "id": "abs_fault",
            "keywords": ["abs", "anti lock"],
            "name_en": "ABS Fault",
            "severity_level": 2,
            "urgency_level": 2,
            "drive_restriction": "Driving allowed with caution",
            "description_en": "The anti-lock braking system is disabled.",
            "action_en": "Drive carefully and check the system soon."
        },
        {
            "id": "esp_fault",
            "keywords": ["esp", "esc", "stability"],
            "name_en": "Stability Control Disabled",
            "severity_level": 1,
            "urgency_level": 1,
            "drive_restriction": "Driving allowed",
            "description_en": "Electronic stability control is inactive.",
            "action_en": "Inspect the system if the issue persists."
        },
        {
            "id": "glow_plug",
            "keywords": ["glow plug", "diesel"],
            "name_en": "Glow Plug Indicator (Diesel)",
            "severity_level": 1,
            "urgency_level": 1,
            "drive_restriction": "Driving allowed",
            "description_en": "Glow plugs are warming the engine.",
            "action_en": "Wait for the light to turn off before starting the engine."
        },
        {
            "id": "dpf_warning",
            "keywords": ["dpf", "filter"],
            "name_en": "Diesel Particulate Filter Warning",
            "severity_level": 3,
            "urgency_level": 2,
            "drive_restriction": "Driving allowed",
            "description_en": "The particulate filter requires regeneration.",
            "action_en": "Perform a 10–20 minute high-speed drive."
        },
        {
            "id": "engine_cold",
            "keywords": ["cold engine"],
            "name_en": "Cold Engine",
            "severity_level": 1,
            "urgency_level": 1,
            "drive_restriction": "Driving allowed",
            "description_en": "The engine has not reached operating temperature.",
            "action_en": "Drive gently until warmed up."
        },
        {
            "id": "door_open",
            "keywords": ["door open"],
            "name_en": "Door Open",
            "severity_level": 1,
            "urgency_level": 1,
            "drive_restriction": "Driving not recommended",
            "description_en": "A door is not fully closed.",
            "action_en": "Close all doors properly."
        },
        {
            "id": "trunk_open",
            "keywords": ["trunk", "boot"],
            "name_en": "Trunk Open",
            "severity_level": 1,
            "urgency_level": 1,
            "drive_restriction": "Driving not recommended",
            "description_en": "The trunk is not fully closed.",
            "action_en": "Close the trunk securely."
        },
        {
            "id": "bonnet_open",
            "keywords": ["hood", "bonnet"],
            "name_en": "Hood Open",
            "severity_level": 2,
            "urgency_level": 1,
            "drive_restriction": "Do not drive",
            "description_en": "The hood is open or not latched.",
            "action_en": "Close the hood securely."
        },
        {
            "id": "washer_fluid_low",
            "keywords": ["washer fluid"],
            "name_en": "Low Washer Fluid",
            "severity_level": 1,
            "urgency_level": 1,
            "drive_restriction": "Driving allowed",
            "description_en": "Windshield washer fluid is low.",
            "action_en": "Refill the washer fluid."
        },
        {
            "id": "low_fuel",
            "keywords": ["fuel", "low fuel"],
            "name_en": "Low Fuel",
            "severity_level": 1,
            "urgency_level": 1,
            "drive_restriction": "Driving allowed",
            "description_en": "Fuel level is low.",
            "action_en": "Refuel soon."
        },
        {
            "id": "seatbelt",
            "keywords": ["seatbelt"],
            "name_en": "Seatbelt Not Fastened",
            "severity_level": 2,
            "urgency_level": 5,
            "drive_restriction": "Do not drive",
            "description_en": "A passenger is not wearing a seatbelt.",
            "action_en": "Ensure all passengers fasten seatbelts."
        },
        {
            "id": "parking_brake",
            "keywords": ["parking brake", "handbrake"],
            "name_en": "Parking Brake Engaged",
            "severity_level": 1,
            "urgency_level": 1,
            "drive_restriction": "Do not drive",
            "description_en": "The parking brake is still engaged.",
            "action_en": "Release the parking brake."
        },
        {
            "id": "trailer_issue",
            "keywords": ["trailer", "tow"],
            "name_en": "Trailer Connection Issue",
            "severity_level": 2,
            "urgency_level": 2,
            "drive_restriction": "Driving allowed with caution",
            "description_en": "There is an electrical or connection issue with the trailer.",
            "action_en": "Check trailer wiring and connector."
        }
    ]

    # Save warning lights JSON
    warning_json_path = base / "warnings" / "warning_lights_full.json"
    warning_json_path.write_text(json.dumps(warning_lights, indent=4), encoding="utf-8")

    print("Knowledge Base structure + full English warning lights JSON created successfully.")


# Execute
create_kb_structure("knowledge_base")
