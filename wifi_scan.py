import wifi
import folium
import tkinter as tk
from tkinter import ttk

# Define the criteria for filtering networks
MIN_SIGNAL_STRENGTH = -80
SECURITY_TYPES = {"wpa", "wpa2"}

# Create a WiFi scanner object
wifi_scanner = wifi.WiFiScan()

# Define a function to update the listbox with the available networks
def update_networks_list():
    networks_list.delete(0, tk.END)
    for network in networks:
        if network.signal_strength > MIN_SIGNAL_STRENGTH and network.security.lower() in SECURITY_TYPES:
            networks_list.insert(tk.END, f"{network.ssid} ({network.signal_strength} dBm, {network.security})")

# Define a function to plot the available networks on a map
def plot_networks_map():
    map_center = (51.5074, -0.1278) # London coordinates
    wifi_map = folium.Map(location=map_center, zoom_start=12)
    for network in networks:
        folium.Marker(location=[network.latitude, network.longitude], popup=f"{network.ssid} ({network.signal_strength} dBm, {network.security})").add_to(wifi_map)
    wifi_map.save("wifi_networks.html")
    tk.messagebox.showinfo(title="WiFi Networks Map", message="The WiFi networks map has been saved to 'wifi_networks.html'")

# Scan for available networks
networks = wifi_scanner.scan()

# Create a GUI window
root = tk.Tk()
root.title("WiFi Scanner")

# Create a listbox to display the available networks
networks_list = tk.Listbox(root)
networks_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a scrollbar for the listbox
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=networks_list.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
networks_list.configure(yscrollcommand=scrollbar.set)

# Create a button to update the list of networks
update_button = ttk.Button(root, text="Update", command=update_networks_list)
update_button.pack(side=tk.TOP, padx=10, pady=10)

# Create a button to plot the networks on a map
plot_button = ttk.Button(root, text="Plot Map", command=plot_networks_map)
plot_button.pack(side=tk.TOP, padx=10, pady=10)

# Update the list of networks
update_networks_list()

# Start the GUI loop
root.mainloop()
