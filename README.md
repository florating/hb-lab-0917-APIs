# Instructions
This does not contain the `secrets.sh` file, which you will need to create.

Lab instructions: [click here](https://fellowship.hackbrightacademy.com/materials/serft8/exercises/apis/)

### Setup:
1. Create a `secrets.sh` file at the same level as `server.py`:
    * Within the file, add the text: `export TICKETMASTER_KEY="YOUR_API_KEY_HERE"`
    * Get your API key [here](https://developer.ticketmaster.com/products-and-docs/apis/getting-started/)
    * View Ticketmaster Documentation [here](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/)
2. In the terminal: `source secrets.sh`
3. In the terminal: `python3 server.py`