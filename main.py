import args
from ntu_tree_crawler import NTU_TreeCrawler
from ntu_elec_crawler import NTU_ElecCrawler
from ntu_building_crawler import NTU_BuildingCrawler
from ntu_airbox_crawler import NTU_AirboxCrawler
from arcgis_events import (GetOneTreeDataEvent,
                           GetAllTreeDataEvent,
                           GetOneElecDataEvent,
                           GetAllElecDataEvent,
                           GetOneBuildingDataEvent,
                           GetAllBuildingDataEvent,
                           GetOneAirboxDataEvent,
                           GetAllAirboxDataEvent,
                           AddAllDataToMap,
                           SaveArcGIS,
                           UploadGIS_Service)


def Main(isGetTreeData, isGetBuildingData, isGetElecData, isGetAirboxData, isToDatabase, isCommit, isToArcGIS, isUploadArcGIS):
    # Crawler objects:
    crawlerT = NTU_TreeCrawler(args.urlAll, args.urlTree, args.urlGet,
                               header = args.header,
                               db = args.databaseName,
                               dbInfo = args.SQL_Info,
                               isToDatabase = isToDatabase,
                               isCommit = isCommit)
    crawlerE = NTU_ElecCrawler(url = args.urlElec,
                               header = args.header,
                               db = args.databaseName,
                               dbInfo = args.SQL_Info,
                               isToDatabase = isToDatabase,
                               isCommit = isCommit)
    crawlerB = NTU_BuildingCrawler(url = args.urlBuilding,
                                   header = args.header,
                                   db = args.databaseName,
                                   dbInfo = args.SQL_Info,
                                   isToDatabase = isToDatabase,
                                   isCommit = isCommit)
    crawlerA = NTU_AirboxCrawler(url = args.urlAirBox,
                                 header = header,
                                 db = args.databaseName,
                                 dbInfo = args.SQL_Info,
                                 isToDatabase = isToDatabase,
                                 isCommit = isCommit)
    args.crawlerT = crawlerT
    args.crawlerB = crawlerB
    args.crawlerE = crawlerE
    args.crawlerA = crawlerA

    # Set data-getting events:
    if isToArcGIS:
        crawlerT.getOneDataEvents.append(GetOneTreeDataEvent)
        crawlerT.getAllDataEvents.append(GetAllTreeDataEvent)
        crawlerE.getOneDataEvents.append(GetOneElecDataEvent)
        crawlerE.getAllDataEvents.append(GetAllElecDataEvent)
        crawlerB.getOneDataEvents.append(GetOneBuildingDataEvent)
        crawlerB.getAllDataEvents.append(GetAllBuildingDataEvent)
        crawlerA.getOneDataEvents.append(GetOneAirboxDataEvent)
        crawlerA.getAllDataEvents.append(GetAllAirboxDataEvent)


    # Main process:
    try:
        # Scrape the tree data:
        if isGetTreeData:
            crawlerT()

        # Scrape the building data:
        if isGetBuildingData:
            crawlerB()

        # Scrape the elec data:
        if isGetElecData:
            crawlerE(*args.elecDataYearRange)

        # Scrape the airbox data:
        if isGetAirboxData:
            crawlerA()

        # ArcGIS actions:
        if isToArcGIS:
            AddAllDataToMap()
            SaveArcGIS()

            # SaveArcGIS() if isToArcGIS == True:
            if isUploadArcGIS:
                UploadGIS_Service()


    except Exception as e:
        print(f'-------\nError in Main:\n  {e}\n-------\n')

    finally:
        if isGetTreeData and not crawlerT.isDatabaseClose:
            crawlerT.CloseDatabase()

        if isGetElecData and not crawlerB.isDatabaseClose:
            crawlerB.CloseDatabase()

        if isGetElecData and not crawlerE.isDatabaseClose:
            crawlerE.CloseDatabase()

        print('='*50)
        print('Done!!\n\n')


if __name__ == "__main__":
    Main(**args.mainControl)

















