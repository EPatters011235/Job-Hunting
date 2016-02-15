import urllib.request as request, urllib.parse as parse
from urllib.parse import urlencode
import json
import xmltodict
from pprint import pprint
import configparser
config = configparser.ConfigParser()
config.read('jobs.cfg') #jobs.cfg is in the working directory of the script
config.sections()

'''
Things to do:
 1) Add in some type of logging so I don't write the same job posting (probably just a text file)
 2) Figure outCB Facet's for multiple locations || Done
 3) Passing a keyword list || Done
 4) Email CB about ExcludeDID option
 5) Add support for other job sites:
    http://www.programmableweb.com/news/70-jobs-apis-indeed-simply-hired-and-careerbuilder/2013/01/23

'''
def career_builder():
    '''
    Takes no variables. Queries Career Builders public API (/jobsearch) for open listings based on my current job criteria.
    Config parser is used to pull the career builder specific api key
    Response type is only XML but is converted to JSON using xmltodict.
    Singing up with CB is a must in order to get a Developer key and access to the APi.
    :return:
    '''
    cb_tmp = []
    cb_url = r'http://api.careerbuilder.com/v1/jobsearch'
    #NOTE: If you are not using a config file, cb_key = <key_value>
    cb_key = config.get('career builder', 'api_key')
    cb_params = {'DeveloperKey': cb_key,
                 'HostSite': 'US', #Necessary in order to search the correct CB site
                 'CountryCode': 'US',
                 'UseFacets': 'true',
                 'FacetCity': ['San Diego, Denver, Phoenix, Scottsdale'],
                 'PerPage': '100',
                 #'ExcludeCompanyNames': 'ManTech International Corporation',
                 'Keywords': 'cyber'} #Only jobs that have all of the key words will match and be returned
    #Encode cb_url, cb_key, and cb_params to proper URL
    cb_url_parts = list(parse.urlparse(cb_url))
    cb_query = dict(parse.parse_qsl(cb_url_parts[4]))
    cb_query.update(cb_params)
    cb_url_parts[4] = urlencode(cb_query)
    #Get encoded URL
    cb_fetch = (parse.urlunparse(cb_url_parts))
    cb_job_data = request.urlopen(cb_fetch)
    #Deconde byte stream to string
    cb_response = cb_job_data.read().decode('utf-8')
    #Convert XMl to JSON because screw creating an XML parser
    xml_input = xmltodict.parse(cb_response)
    cb_json_input = json.dumps(xml_input)
    cb_json_output = json.loads(cb_json_input)
    pprint(cb_json_output)
    #Bevs on the beach
    for jobs in cb_json_output['ResponseJobSearch']['Results']['JobSearchResult']:
        job_title = {'title': jobs['JobTitle']}.get('title', 'Missing')
        description = {'description': jobs['DescriptionTeaser']}.get('description', 'Missing')
        city = {'city': jobs['City']}.get('city', 'Missing')
        state = {'state': jobs['State']}.get('state', 'Missing')
        emp_type = {'emp_type': jobs['EmploymentType']}.get('emp_type', 'Missing')
        job_url = {'job_url': jobs['JobDetailsURL']}.get('job_url', 'Missing')
        salary = {'salary': jobs['Pay']}.get('salary', 'Missing')
        #Probably a better way to handle this but oh well
        if type(jobs['Skills']['Skill']) == list:
            skills = {'skills': ', '.join(jobs['Skills']['Skill'])}.get('skills', 'Missing')
        else:
            skills = {'skills': str(jobs['Skills']['Skill'])}.get('skills', 'Missing')
            print(skills)
        cb_data = [job_title,
                   description,
                   city,
                   state,
                   emp_type,
                   job_url,
                   salary,
                   skills]
        cb_tmp.append(cb_data)
        pprint(jobs)
    return cb_tmp
def file_creator(cb_tmp):
    ################################################################
    #   Will have more job websites eventually, with each website  #
    #   having its own excel sheet.                                #
    ################################################################
    import xlwt
    wb = xlwt.Workbook()
    if cb_tmp:
        #Write headers
        cb_ws = wb.add_sheet('Career Builder')
        cb_headers = ['Job Title', 'Description', 'City', 'State', 'Employment Type', 'Job URL', 'Salary', 'Skills']
        (x, y) = (0, 0)
        for cb_column in cb_headers:
            cb_ws.write(x, y, cb_column)
            y += 1
        #Reset Counter
        del (x, y)
        (x, y) = (0, 0)
        #Write row values
        for cb_row in cb_tmp:
            x += 1
            for cb_row_value in cb_row:
                cb_ws.write(x, y, cb_row_value)
                y += 1
            y = 0
        #Reset Counter
        del (x, y)
    else:
        pass
    #Path to output file
    wb.save('E:\Documents\\' + 'jobs.xls')

def monster():
    pass

def indeed():
    pass


def get_jobs():
    cb_tmp = career_builder()
    file_creator(cb_tmp)
if __name__ == '__main__':
    get_jobs()

