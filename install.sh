#!/bin/bash

echo "Installing System Monitor Dashboard..."

sudo apt update
sudo apt install python3-pip -y

pip3 install -r requirements.txt

echo "Installation complete!"
echo "Run the dashboard with:"
echo "python3 -m streamlit run dashboard.py"