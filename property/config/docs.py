source_link = "https://github.com/osstechnolab/property"
docs_base_url = "https://osstechnolab.github.io/property"
headline = "PropertyNext"
sub_heading = "Property Management App for ERPNext"
long_description = """(long description in markdown)"""

def get_context(context):
    # optional settings

    # context.brand_html = 'Brand info on the top left'
    # context.favicon = 'path to favicon'
    #
    context.top_bar_items = [
      {"label": "About", "url": context.docs_base_url + "/about"},
    ]

pass

"""
Configuration for docs
"""

# source_link = "https://github.com/[org_name]/property"
# docs_base_url = "https://[org_name].github.io/property"
# headline = "App that does everything"
# sub_heading = "Yes, you got that right the first time, everything"

def get_context(context):
	context.brand_html = "Property"
