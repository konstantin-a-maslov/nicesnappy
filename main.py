import nicesnappy
from nicesnappy import Read, Write, Chain, Branches, Map, Zip, SNAPOperator


def get_processing_graph(mst_input_path, slv_input_path, output_path):
    apply_orbit_file = SNAPOperator("Apply-Orbit-File")
    split_1 = SNAPOperator("TOPSAR-Split", {"subswath": "IW1"})
    split_2 = SNAPOperator("TOPSAR-Split", {"subswath": "IW2"})
    split_3 = SNAPOperator("TOPSAR-Split", {"subswath": "IW3"})
    back_geocoding = SNAPOperator("Back-Geocoding", {
        "maskOutAreaWithoutElevation": "false",
        "demName": "Copernicus 30m Global DEM"
    })
    deburst = SNAPOperator("TOPSAR-Deburst")
    merge = SNAPOperator("TOPSAR-Merge")
    interferogram = SNAPOperator("Interferogram", {"demName": "Copernicus 30m Global DEM"})
    # terrain_correction = SNAPOperator("Terrain-Correction", {
    #     "demName": "Copernicus 30m Global DEM",
    #     "pixelSpacingInMeter": "10"
    # })

    graph = Chain([
        Branches([
            Read(mst_input_path),
            Read(slv_input_path)
        ]),
        Map(apply_orbit_file),
        Map(
            Branches([
                split_1,
                split_2,
                split_3
            ])
        ),
        Zip(back_geocoding),
        Map(deburst),
        merge,
        interferogram,
        # terrain_correction,
        Write(output_path, "BEAM-DIMAP")
    ])
    return graph


def main():
    nicesnappy.initialize("/home/konstantin/.snap/snap-python")
    # nicesnappy.initialize("<path/to/snappy>") # e.g. "/home/konstantin/.snap/snap-python"
    # you can also import snappy as you like and initialize nicesnappy 
    # by sending the module as a parameter to nicesnappy.initialize_with_module
    
    mst_path = "S1A_IW_SLC__1SDV_20150814T171453_20150814T171510_007262_009F26_1FC0.zip"
    slv_path = "S1A_IW_SLC__1SDV_20150826T171454_20150826T171510_007437_00A3E8_6B98.zip"
    output_path = "interferogram_20150814_20150826"

    processing_graph = get_processing_graph(mst_path, slv_path, output_path)
    processing_graph.apply()


if __name__ == "__main__":
    main()
