import base64
from pathlib import Path
import pandas as pd
import sel
import altair as alt
import streamlit as st
import datetime
from dateutil.relativedelta import relativedelta

def streamlit_theme():
    font = "IBM Plex Mono"
    primary_color = "#F63366"
    font_color = "#262730"
    grey_color = "#f0f2f6"
    base_size = 16
    lg_font = base_size * 1.25
    sm_font = base_size * 0.8  # st.table size
    xl_font = base_size * 1.75  # noqa

    config = {
        "config": {
            "arc": {"fill": primary_color},
            "area": {"fill": primary_color},
            "circle": {"fill": primary_color, "stroke": font_color, "strokeWidth": 0.5},
            "line": {"stroke": primary_color},
            "path": {"stroke": primary_color},
            "point": {"stroke": primary_color},
            "rect": {"fill": primary_color},
            "shape": {"stroke": primary_color},
            "symbol": {"fill": primary_color},
            "title": {
                "font": font,
                "color": font_color,
                "fontSize": lg_font,
                "anchor": "start",
            },
            "axis": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
                "gridColor": grey_color,
                "domainColor": font_color,
                "tickColor": "#fff",
            },
            "header": {
                "labelFont": font,
                "titleFont": font,
                "labelFontSize": base_size,
                "titleFontSize": base_size,
            },
            "legend": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
            },
            "range": {
                "category": ["#f63366", "#fffd80", "#0068c9", "#ff2b2b", "#09ab3b"],
                "diverging": [
                    "#850018",
                    "#cd1549",
                    "#f6618d",
                    "#fbafc4",
                    "#f5f5f5",
                    "#93c5fe",
                    "#5091e6",
                    "#1d5ebd",
                    "#002f84",
                ],
                "heatmap": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ramp": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ordinal": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
            },
        }
    }
    return config


def streamlit_theme_alt():
    font = "IBM Plex Mono"
    primary_color = "#F63366"
    font_color = "#262730"
    grey_color = "#f0f2f6"
    base_size = 16
    lg_font = base_size * 1.25
    sm_font = base_size * 0.8  # st.table size
    xl_font = base_size * 1.75  # noqa

    config = {
        "config": {
            "view": {"fill": grey_color},
            "arc": {"fill": primary_color},
            "area": {"fill": primary_color},
            "circle": {"fill": primary_color, "stroke": font_color, "strokeWidth": 0.5},
            "line": {"stroke": primary_color},
            "path": {"stroke": primary_color},
            "point": {"stroke": primary_color},
            "rect": {"fill": primary_color},
            "shape": {"stroke": primary_color},
            "symbol": {"fill": primary_color},
            "title": {
                "font": font,
                "color": font_color,
                "fontSize": lg_font,
                "anchor": "start",
            },
            "axis": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
                "grid": True,
                "gridColor": "#fff",
                "gridOpacity": 1,
                "domain": False,
                # "domainColor": font_color,
                "tickColor": font_color,
            },
            "header": {
                "labelFont": font,
                "titleFont": font,
                "labelFontSize": base_size,
                "titleFontSize": base_size,
            },
            "legend": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
            },
            "range": {
                "category": ["#f63366", "#fffd80", "#0068c9", "#ff2b2b", "#09ab3b"],
                "diverging": [
                    "#850018",
                    "#cd1549",
                    "#f6618d",
                    "#fbafc4",
                    "#f5f5f5",
                    "#93c5fe",
                    "#5091e6",
                    "#1d5ebd",
                    "#002f84",
                ],
                "heatmap": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ramp": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ordinal": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
            },
        }
    }
    return config


category_large = [
    "#f63366",
    "#0068c9",
    "#fffd80",
    "#7c61b0",
    "#ffd37b",
    "#ae5897",
    "#ffa774",
    "#d44a7e",
    "#fd756d",
]

alt.themes.register("streamlit", streamlit_theme)
alt.themes.enable("streamlit")

colnames_item = ['pid', 'b_name', 'title', 'size', 'og_price', 'new_price', 'sold_price', 'is_sold', 'old_date', 'new_date', '%p_change', 'Link']
colnames_seller = ['uname', 'ship_cost', 'amt_sold', 'amt_feedback', 'amt_listings', 'desc', 'amt_likes', 'prf_link', 'feed_link', 'size_desc', 'loc', 'amt_pics', 'Link']

colnames = {
    "pid": "Product ID",
    "b_name": "Brand Name",
    "title": "Title of Listing",
    "size": "Product Tag Size",
    "og_price": "Original Price of Listing",
    "new_price": "New Price of Listing",
    "sold_price": "Price if Listing Sold",
    "is_sold": "Boolean if Listing Sold",
    "old_date": "Original Date Listing was Created",
    "new_date": "Last Time Listing was Bumped",
    "%p_change": "Price Change (%) if Listing Lowered Prices",
    "link": "Original Link of Listing",
    "uname": "Username of Seller",
    "ship_cost": "Cost of Shipping",
    "amt_sold": "Total Number of Items Sold",
    "amt_feedback": "Total Number of Feedback Received",
    "amt_listings": "Total Number of Listings from Seller",
    "desc": "Full Text Description of Listing",
    "amt_likes": "Total Number of Favorites on Listing",
    "prf_link": "Link to Seller's Profile",
    "feed_link": "Link to Seller's Feedback",
    "size_desc": "Full Description to Listing's Size",
    "loc": "Location of Seller (where it's shipped from)",
    "amt_pics": "Number of Pictures in Listing"
}


"""
returns datetime with "X Ago" to relative date from a string
org_date: original date to be converted (str)
"""
def normalize_date(org_date):

    if org_date == "na" or org_date == "nan" or pd.isnull(org_date) or len(org_date.split()) == 1:
        return "nan"

    fixed = org_date.replace("Sold", "").replace("almost", "").replace("over", "")
    splitted = fixed.split()

    TODAY = datetime.date.today()

    if len(splitted) == 1 and splitted[0].lower() == 'today':
        return str(TODAY.isoformat())
    elif len(splitted) == 1 and splitted[0].lower() == 'yesterday':
        date = TODAY - relativedelta(days=1)
        return str(date.isoformat())
    elif splitted[1].lower() in ['hour', 'hours', 'hr', 'hrs', 'h']:
        date = datetime.datetime.now() - relativedelta(hours=int(splitted[0]))
        return str(date.date().isoformat())
    elif splitted[1].lower() in ['minute', 'minutes', 'm', 'min']:
        date = datetime.datetime.now() - relativedelta(minutes=int(splitted[0]))
        return str(date.date().isoformat())
    elif splitted[1].lower() in ['day', 'days', 'd']:
        date = TODAY - relativedelta(days=int(splitted[0]))
        return str(date.isoformat())
    elif splitted[1].lower() in ['wk', 'wks', 'week', 'weeks', 'w']:
        date = TODAY - relativedelta(weeks=int(splitted[0]))
        return str(date.isoformat())
    elif splitted[1].lower() in ['mon', 'mons', 'month', 'months', 'm']:
        date = TODAY - relativedelta(months=int(splitted[0]))
        return str(date.isoformat())
    elif splitted[1].lower() in ['yrs', 'yr', 'years', 'year', 'y']:
        date = TODAY - relativedelta(years=int(splitted[0]))
        return str(date.isoformat())
    else:
        return "Wrong Argument format"

"""
date_list has to be a pandas series
"""
def convert_date_series(d_series):
    return d_series.apply(lambda x: get_past_date(x))

"""
adds "final_price" variable, which consolidates:
1. keeps org_price if listing not sold or updated price
2. keeps new_price if listing not sold
3. keeps sold_price if listing sold
"""
def fix_new_price(sold_prices, new_prices, is_sold, og_price):
    fixed = [x if (z == True) else y for (x,y,z) in zip(sold_prices, new_prices, is_sold) ]
    #now add final_price if only has original_price (not sold and price hasn't changed)
    final_price = [y.replace("$", "").replace(",", "") if (pd.isnull(x) or pd.isna(x) or x == "NA") else x.replace("$", "").replace(",", "") for (x,y) in zip(fixed, og_price)]
    return final_price


def get_table_download_link(df, user_input):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<center><a href="data:file/csv;base64,{b64}" download="{user_input}.csv">Download .csv file </a></center>'
    return href

##### CHARTS ####

def graph_timeseries(df, titl):
    #make sure both new columns are included:
    df['final_price'] = fix_new_price(df['sold_price'], df['new_price'], df['is_sold'], df['og_price'])
    df['final_price'] = df['final_price'].astype(int)

    df['normalized_date'] = df['new_date'].apply(lambda x: normalize_date(x))
    df['normalized_date'] = pd.to_datetime(df['normalized_date'])

    #graph:
    selection = alt.selection_single(); #chooses which selection methods are possible

    chart = alt.Chart(df).mark_point(filled=False).encode(
        alt.X('normalized_date:T', scale=alt.Scale(zero=False), axis=alt.Axis(title='date')),
        alt.Y('final_price:Q', scale=alt.Scale(zero=False), axis=alt.Axis(format = "$.2f", title='price($)')),
        alt.Size('amt_likes:Q'),
        alt.Order('amt_likes:Q', sort='descending'),
        tooltip = [alt.Tooltip('uname'),
                alt.Tooltip('title'),
                alt.Tooltip('size'),
                alt.Tooltip('og_price:N'),
                alt.Tooltip('final_price:Q'),
                alt.Tooltip('normalized_date:T'),
                alt.Tooltip('is_sold'),
                alt.Tooltip('%p_change:N'),
                #alt.Tooltip('ship_cost:N'),
                alt.Tooltip('amt_likes:N'),
                alt.Tooltip('amt_feedback:N'),
                #alt.Tooltip('desc')
                ],
        color=alt.condition(selection, 'is_sold', alt.value('grey'))
        ).add_selection(selection).properties(
        width = 700,
        height = 350,
        title = titl + " (Price over time)"
        )

    return chart


def to_altair_datetime(dt):
    dt = pd.to_datetime(dt)
    return alt.DateTime(year=dt.year, month=dt.month, date=dt.day,
                        hours=dt.hour, minutes=dt.minute, seconds=dt.second,
                        milliseconds=0.001 * dt.microsecond)

def graph_timeseries_domain(df,date1,date2, titl):
    #make sure both new columns are included:
    df['final_price'] = fix_new_price(df['sold_price'], df['new_price'], df['is_sold'], df['og_price'])
    df['final_price'] = df['final_price'].astype(int)

    df['normalized_date'] = df['new_date'].apply(lambda x: normalize_date(x))
    df['normalized_date'] = pd.to_datetime(df['normalized_date'])

    #graph:
    selection = alt.selection_single(); #chooses which selection methods are possible

    domain = [to_altair_datetime(date1),
          to_altair_datetime(date2)]

    chart = alt.Chart(df).mark_point(clip = True, filled=False).encode(
        alt.X('normalized_date:T', scale=alt.Scale(zero=False, domain = domain), axis=alt.Axis(title='date')),
        alt.Y('final_price:Q', scale=alt.Scale(zero=False), axis=alt.Axis(format = "$.2f", title='price ($)')),
        alt.Size('amt_likes:Q'),
        alt.Order('amt_likes:Q', sort='descending'),
        tooltip = [alt.Tooltip('uname'),
                alt.Tooltip('title'),
                alt.Tooltip('size'),
                alt.Tooltip('og_price:N'),
                alt.Tooltip('final_price:Q'),
                alt.Tooltip('normalized_date:T'),
                alt.Tooltip('is_sold'),
                alt.Tooltip('%p_change:N'),
                #alt.Tooltip('ship_cost:N'),
                alt.Tooltip('amt_likes:N'),
                alt.Tooltip('amt_feedback:N'),
                #alt.Tooltip('desc')
                ],
        color=alt.condition(selection, 'is_sold', alt.value('grey'))
        ).add_selection(selection).properties(
        width = 700,
        height = 350,
        title = titl + " (Price over time)"
        )

    chart.configure_header(
    titleColor='green',
    titleFontSize=14,
    labelColor='red',
    labelFontSize=14
    )

    return chart
#######

#@st.cache
def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

#@st.cache
def display_picture(link, length, width, is_sold):
    image_link = sel.get_image(link, is_sold)
    picture_html = f"<center><img src='{image_link}' class='img-fluid' width = '{width}' length = '{length}'></center>"
    st.markdown(picture_html, unsafe_allow_html=True)

def get_image_links(df):
    links = df['Link']
    is_sold_list = df['is_sold']
    image_links = [ f"<center><img src='{sel.get_image(x,y)}' class='img-fluid' width = '{100}' length = '{100}'></center>" for (x,y) in zip(links, is_sold_list)]
    return image_links

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
