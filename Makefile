ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/
INPUTS:=$(ROOT_DIR)Data/Input/
OUTPUTS:=$(ROOT_DIR)Data/Output/

# Analyze images
analyze_images:
	python $(ROOT_DIR)Scripts/analyze_images.py $(ROOT_DIR) "No"
analyze_images_full:
	python $(ROOT_DIR)Scripts/analyze_images.py $(ROOT_DIR) "Yes"

# Create graphs
create_graphs:
	python $(ROOT_DIR)Scripts/create_graphs.py $(INPUTS) $(OUTPUTS)




# Code to replicate:
sync_local_to_remote_data:
	rsync -ave ssh /home/scott/Documents/Uni/Research/Projects/Blueberry_Network_Rewiring/data --chmod=Dg+s teresisc@rsync.hpcc.msu.edu:/mnt/research/edgerpat_lab/Scotty/Blueberry_Network_Rewiring/

sync_local_to_remote_results:
	rsync -ave ssh /home/scott/Documents/Uni/Research/Projects/Blueberry_Network_Rewiring/results --chmod=Dg+s teresisc@rsync.hpcc.msu.edu:/mnt/research/edgerpat_lab/Scotty/Blueberry_Network_Rewiring/
	

