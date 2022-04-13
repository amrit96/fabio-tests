from models import Continent, Country, City
from db_operations import add_data, get_data, update_data, delete_data

region_table = {'continent': Continent, 'country': Country, 'city': City}
parent_region = {'continent': None, 'country': (Continent, 'continent'), 'city': (Country, 'country')}

def add_continent(name, population, area):
    """
    this method will add continet with proper validation
    Args:
        name: name of continent
        population: population of continent
        area: area of the continent

    Returns:
        success/failure message
    """
    region_validation = validate_region_for_add(region_type='continent', entry_region=name, entry_area=area,
                                                entry_population=population)
    if region_validation == 'valid':
        try:
            continent = Continent(name=name, population=population, area=area)
            add_data.delay(continent)
            result = "Success"
        except Exception as e:
            result = f"Failure: {str(e)}"
    else:
        result = region_validation
    return result


def add_country(name, population, area, continent_id, hospital_count=0, national_park=0):
    """
    this method will be used to add a new country with proper validation
    Args:
        name: name of country
        population: country's population
        area: area of the country
        continent_id: id of the continent of which the country is a part
        hospital_count: number of hospitals in the country
        national_park: number of national park in the country

    Returns:
         success/failure message
    """

    region_validation = validate_region_for_add(region_type='country', entry_region=name, entry_area=area,
                                                entry_population=population, parent_region_name=continent_id)
    if region_validation == 'valid':
        try:
            country = Country(name=name, population=population, area=area, hospital_count=hospital_count,
                              national_park=national_park, continent=continent_id)
            add_data.delay(country)
            result = "Success"
        except Exception as e:
            result = f"Failure: {str(e)}"
    else:
        result = region_validation
    return result


def add_city(name, population, area, country_id, road_count=0, tree_count=0):
    """
    this method will be used to add new cities with proper basic validation
    Args:
        name: name of the city
        population: city's population
        area: area of the city
        country_id: id of the country of which this city is a part of
        road_count: number of roads in the city
        tree_count: number of trees in the city

    Returns:
         success/failure message
    """
    region_validation = validate_region_for_add(region_type='city', entry_region=name, entry_area=area,
                                                entry_population=population, parent_region_name=country_id)
    if region_validation == 'valid':
        try:
            country = City(name=name, population=population, area=area, tree_count=tree_count, road_count=road_count,
                           continent=country_id)
            add_data.delay(country)
            result = "Success"
        except Exception as e:
            result = f"Failure: {str(e)}"
    else:
        result = region_validation
    return result


def validate_region_for_add(region_type, entry_region, entry_area, entry_population, parent_region_name=None):
    """
    this method will be used to conduct basic validation before addition of any region
    Args:
        region_type: type of region: continent/countruy/city
        entry_region: name of the region
        entry_area: size of the region
        entry_population: region's population
        parent_region_name: id of it's containing region(applicable for city and country only)

    Returns:
        valid / appropriate error message
    """

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
    """
    this method will be used to update existing data of any region
    Args:
        region_type: type of region: continent/countruy/city
        region_id: id(primary_key) of the region
        property_name: name of the property to be altered
        property_value: updated value of the property

    Returns:
        success/failure messgae
    """
    region_validation = validate_existing_region(region_type=region_type, region_id=region_id,
                                                 property_name=property_name, property_value=property_value)
    if region_validation == 'valid':
        try:
            updated_data = {getattr(region_table[region_type], property_name): property_value}
            update_data.delay(table_name=region_table[region_type], data_object=updated_data, id_value=region_id)
            result = "Success"
        except Exception as e:
            result = f"Failure: {str(e)}"
    else:
        result = region_validation
    return result


def validate_existing_region(region_type, region_id, property_name=None, property_value=None):
    """
    this method will be used to validate any existing region before update or delete
    Args:
        region_type: type of region: continent/countruy/city
        region_id: id(primary_key) of the region
        property_name: name of the property to be altered
        property_value: updated value of the property

    Returns:
        valid / appropriate error message
    """
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
    """
    this method will be used to fetch region details (all/filtered)
    Args:
        region_type: type of region: continent/countruy/city
        filter_by: name of the column against which the filtering is to be done
        filter_value:  value of the filtering column

    Returns:
        a list of dictionary if data is present. else appropriate error message is returned
    """
    try:
        result = get_data(table_name=region_table[region_type], filter_key=filter_by, filter_value=filter_value)
        if not result:
            result = 'No Data Found'
    except Exception as e:
        result = f"Failed to fetch data: {str(e)}"
    return result

def remove_region(region_type, region_id):
    """
    this method is used to remove any existion region from db
    Args:
        region_type: type of region: continent/countruy/city
        region_id: id(primary_key) of the region

    Returns:
        success / appropriate error message
    """
    valid_region = validate_existing_region(region_type=region_type, region_id=region_id)
    if valid_region == 'valid':
        try:
            delete_data.delay(table_name=region_table[region_type], id_value=region_id)
            result = "success"
        except Exception as e:
            result = f"Failed to remove {region_type}"
    else:
        result = "Invalid Id"
    return result



