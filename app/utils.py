from models import Continent, Country, City
from db_operations import add_data, get_data, update_data, delete_data

region_table = {'continent': Continent, 'country': Country, 'city': City}
parent_region = {'continent': None, 'country': (Continent, 'continent'), 'city': (Country, 'country')}

def add_continent(name, population, area):
    region_validation = validate_region_for_add(region_type='continent', entry_region=name, entry_area=area,
                                                entry_population=population)
    if region_validation == 'valid':
        try:
            continent = Continent(name=name, population=population, area=area)
            add_data(continent)
            result = "Success"
        except Exception as e:
            result = f"Failure: {str(e)}"
    else:
        result = region_validation
    return result


def add_country(name, population, area, continent_name, hospital_count=0, national_park=0):

    region_validation = validate_region_for_add(region_type='country', entry_region=name, entry_area=area,
                                                entry_population=population, parent_region_name=continent_name)
    if region_validation == 'valid':
        try:
            country = Country(name=name, population=population, area=area, hospital_count=hospital_count,
                              national_park=national_park, continent=continent_name)
            add_data(country)
            result = "Success"
        except Exception as e:
            result = f"Failure: {str(e)}"
    else:
        result = region_validation
    return result


def add_city(name, population, area, country_name, road_count=0, tree_count=0):
    region_validation = validate_region_for_add(region_type='city', entry_region=name, entry_area=area,
                                                entry_population=population, parent_region_name=country_name)
    if region_validation == 'valid':
        try:
            country = City(name=name, population=population, area=area, tree_count=tree_count, road_count=road_count,
                           continent=country_name)
            add_data(country)
            result = "Success"
        except Exception as e:
            result = f"Failure: {str(e)}"
    else:
        result = region_validation
    return result


def validate_region_for_add(region_type, entry_region, entry_area, entry_population, parent_region_name=None):

    get_region = get_data(table_name=region_table[region_type], filter_key='name', filter_value=entry_region)
    if get_region:
        result = f"Existing {region_type} name"
    else:
        if not parent_region[region_type]:
            result = "Valid"
        else:
            get_parent_region = get_data(table_name=parent_region[region_type][0], filter_key='name', filter_value=parent_region_name)
            parent_id = get_parent_region[0]['id']
            parent_area = get_parent_region[0]['area']
            parent_population = get_parent_region[0]['population']
            get_sibling_region = get_data(table_name=region_table[region_type],
                                          filter_key=parent_region[region_type][1], filter_value=parent_id)

            total_area, total_population = 0, 0
            for region in get_sibling_region:
                total_area += region['area']
                total_population += region['population']
            total_population += entry_population
            total_area += entry_area

            if total_population > parent_population:
                result = "Invalid population data"
            elif total_area > parent_area:
                result = "Invalid area data"
            else:
                result = 'valid'
    return result


def update_region(region_type, region_id, property_name, property_value):
    region_validation = validate_existing_region(region_type=region_type, region_id=region_id,
                                                 property_name=property_name, property_value=property_value)
    if region_validation == 'valid':
        try:
            updated_data = {getattr(region_table[region_type], property_name): property_value}
            update_data(table_name=region_table[region_type], data_object=updated_data, id_value=region_id)
            result = "Success"
        except Exception as e:
            result = f"Failure: {str(e)}"
    else:
        result = region_validation
    return result

def validate_existing_region(region_type, region_id, property_name=None, property_value=None):
    get_region = get_data(table_name=region_table[region_type], filter_key='id', filter_value=region_id)
    shared_property = ['area', 'population']
    if not get_region:
        result = "Invalid ID"
    elif property_name in shared_property:
        if parent_region[region_type]:
            parent_id = get_region[0][parent_region[region_type][0]]
            get_parent = get_data(table_name=parent_region[region_type][0], filter_key=id, filter_value=parent_id)[0]
            get_sibling_region = get_data(table_name=region_table[region_type],
                                          filter_key=parent_region[region_type][1], filter_value=parent_id)
            total_property = 0
            for region in get_sibling_region:
                if region['id'] == region_id:
                    total_property += property_value
                else:
                    total_property += region[property_name]

            if total_property > get_parent[property_name]:
                result = f"Invalid {property_name} data"
            else:
                result = 'valid'
        else:
            result = 'valid'
    else:
        result = 'valid'
    return result


def get_region_details(region_type, filter_by=None, filter_value=None):
    try:
        result = get_data(table_name=region_table[region_type], filter_key=filter_by, filter_value=filter_value)
        if not result:
            result = 'No Data Found'
    except Exception as e:
        result = f"Failed to fetch data: {str(e)}"
    return result

def remove_region(region_type, region_id):
    valid_region = validate_existing_region(region_type=region_type, region_id=region_id)
    if valid_region == 'valid':
        try:
            delete_data(table_name=region_table[region_type], id_value=region_id)
            result = "success"
        except Exception as e:
            result = f"Failed to remove {region_type}"
    else:
        result = "Invalid Id"
    return result



