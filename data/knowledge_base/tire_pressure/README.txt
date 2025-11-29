This folder contains structured tire pressure data for all supported vehicles.
The file 'tire_pressures.json' stores all tire pressure values in a single place.
Format:
{
   "Manufacturer_Model_Year": {
       "front": "XX psi",
       "rear": "YY psi"
   }
}
LLM Note: This is a high-frequency lookup dataset used for fast tire pressure answers.