import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import re
#import datefinder
import time
import sys
import requests
import pickle

#bs4
#from bs4 import BeautifulSoup
#from fake_useragent import UserAgent

import streamlit as st
import altair as alt
import sel
import utils
import datetime
from dateutil.relativedelta import relativedelta

DIRECTORY_PATH = r"C:\Users\ferdi\Downloads\projects\grailed"
FILE_PATH = "\supreme.csv" #edit
from pprint import pformat

#######################################
#FUTURE PLANS:
#0: first thing to do after reading early docs: https://docs.streamlit.io/en/stable/tutorial/create_a_data_explorer_app.html
#1. github actions to automate changes?
#2. create cache where we store all past data and load in cache from user input (https://docs.streamlit.io/en/stable/api.html#streamlit.cache)
#3. long-term retention of testing the app: https://blog.streamlit.io/testing-streamlit-apps-using-seleniumbase/
#4. change theme and configuration through [theme] in https://docs.streamlit.io/en/stable/streamlit_configuration.html
#5. change plots that are in utils.

######## INTRO AND HEADER ########

header_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
    utils.img_to_bytes("images/header.jpg"))

st.markdown(header_html, unsafe_allow_html = True)

intro_markdown = utils.read_markdown_file("markdowns/intro.md")

st.markdown(intro_markdown, unsafe_allow_html = True)

########### SIDE BAR ###############
st.sidebar.markdown("## Configuration")
st.sidebar.markdown("① ** What Listing or Brand to Analyze?**")
user_input = st.sidebar.text_input(label="Enter Product or Brand Name")
amount_scrape = st.sidebar.number_input(label = "Amount of Listings? (Integers Only!)")
#filters
st.sidebar.markdown("② **Apply Filters to Data**")
filter_options = ["Sold Only", "Unsold Only"]
help_list = ["Includes only listings that are sold", "Include only listings that are not sold"]
check_boxes = [st.sidebar.checkbox(option, key=option, help = help_option) for option,help_option in zip(filter_options, help_list)]
#st.sidebar.markdown("_")
st.sidebar.markdown(":clipboard: **Analysis Filters**")
df_filter_options = ["Summarized Dataframe", "Include Graphs"]
df_help_list = ["Includes summarized df that has pictures and key features", "Graphs price over time"]
df_check_boxes = [st.sidebar.checkbox(option, key=option, help = help_option) for option,help_option in zip(df_filter_options, df_help_list)]
st.sidebar.markdown("*Graph Domain Filters (x-axis range)*")
domain_input1 = st.sidebar.text_input(label="Enter Starting Date (in MM-DD-YYYY format)")
domain_input2 = st.sidebar.text_input(label="Enter Ending Date (in MM-DD-YYYY format)")
#TESTING PURPOSES
if st.sidebar.button("test fanilo's function here"):
    sel.test_st()

st.sidebar.markdown("---")

#details
st.sidebar.markdown("ℹ️: ** Details **")
desc_check = st.sidebar.checkbox("Dataset Description")
desc_markdown = utils.read_markdown_file("markdowns/data_description.md")
dict_check = st.sidebar.checkbox("Data Dictionary")
dict_markdown = utils.read_markdown_file("markdowns/data_dictionary.md")

if desc_check:
    st.sidebar.markdown(desc_markdown, unsafe_allow_html=True)
if dict_check:
    st.sidebar.markdown(dict_markdown, unsafe_allow_html=True)
    st.sidebar.code(pformat(utils.colnames, indent=2))
st.sidebar.markdown("_")
#diosclaimer
st.sidebar.markdown(":warning: **Disclaimer:** The acceptable use policy for grailed.com [does not officially allow for web scrapers](https://www.grailed.com/acceptable). This app is purely for educational purposes to learn about underlying trends surrounding clothes.")
st.sidebar.markdown("*Please* use this app at your own discretion, especially for non-nefarious and non-profit purposes. ")


########## MAIN PAGE ##############
st.markdown("_")
faq = st.beta_expander("FAQ:", expanded = True)
faq_md = utils.read_markdown_file("markdowns/faq.md")
faq.markdown(faq_md, unsafe_allow_html = True)


latest_iteration = st.empty()
st.markdown("\n")
st.markdown("\n")
col1, col2, col3 = st.beta_columns([1,1,1])

if check_boxes[0] and check_boxes[1]:
    st.header("** &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp&nbsp;&nbsp;&nbsp;Please check only one filter at a time!**")

elif len(user_input) > 0 and amount_scrape > 0 and amount_scrape < 500 and amount_scrape.is_integer():

    col1.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp; &nbsp;     :link:")
    #col3.write(":o:")
    st.markdown("\n")
    if col2.button("Click Here to Get Data!"):
        latest_iteration = st.empty()
        latest_iteration.markdown('Initiating Scraping... (this may take awhile so go ahead and get a snack :cookie:)')
        bar = st.progress(1)

        #scrape
        if check_boxes[0]:
            sold_df = sel.scrape_filter_sold(user_input, amount_scrape)
        elif check_boxes[1]:
            unsold_df = sel.scrape(user_input, amount_scrape)
        else:
            unsold_df = sel.scrape(user_input, amount_scrape)
            sold_df = sel.scrape_filter_sold(user_input, amount_scrape)

        for i in range(1, 100):
          latest_iteration.text(f'Getting data... {i+1}%')
          bar.progress(i + 1)
          time.sleep(.01)

        if not check_boxes[0] and not check_boxes[1]: #Shows both sold and unsold listings
            #merge
            merged_df = sel.merge_df(user_input, unsold_df, sold_df)
            merge_iteration = st.empty()
            merge_bar = st.progress(0)

            for i in range(100):
              merge_iteration.text(f'Merging data... {i+1}%')
              merge_bar.progress(i + 1)
              time.sleep(.01)
            st.success("Data Retrieved!")

            first_listing_link = list(merged_df['Link'])[0]
            utils.display_picture(first_listing_link, 500, 400, False)
            merged_df['image_links'] = utils.get_image_links(merged_df)

            st.subheader("Dataframe:")
            st.write(merged_df)

            if df_check_boxes[0]:
                #latest_iteration.markdown('Getting pictures and summarized df... (this may take awhile so go ahead and get a second snack :cookie:)')
                merged_df['final_price'] = utils.fix_new_price(merged_df['sold_price'], merged_df['new_price'], merged_df['is_sold'], merged_df['og_price'])
                filtered_df = merged_df[['title', 'final_price', 'image_links']]
                st.write(filtered_df.to_html(escape=False), unsafe_allow_html=True)
            st.markdown(utils.get_table_download_link(merged_df, user_input), unsafe_allow_html=True) #download link

            if df_check_boxes[1]: #graphs
                dcol1, dcol2,dcol3 = st.beta_columns(3)
                dcol1.altair_chart(utils.graph_timeseries(merged_df, user_input))

                st.markdown("Filtered Graph:")
                if len(domain_input1) > 0 and len(domain_input2) > 0:
                    dcol1.altair_chart(utils.graph_timeseries_domain(merged_df, domain_input1, domain_input2, user_input))


        elif check_boxes[0]: #Shows only sold listings
            st.success("Data Retrieved!")

            first_listing_link = list(sold_df['Link'])[0]
            utils.display_picture(first_listing_link , 500, 400, True)

            st.subheader("Dataframe:")
            st.write(sold_df)

            if df_check_boxes[0]:
                latest_iteration.markdown('Getting pictures and summarized df... (this may take awhile so go ahead and get a second snack :cookie:)')
                sold_df['final_price'] = utils.fix_new_price(sold_df['sold_price'], sold_df['new_price'], sold_df['is_sold'], sold_df['og_price'])
                filtered_df = sold_df[['title', 'final_price', 'image_links']]
                st.write(filtered_df.to_html(escape=False), unsafe_allow_html=True)

            st.markdown(utils.get_table_download_link(sold_df, user_input), unsafe_allow_html=True)

            if df_check_boxes[1]:
                dcol1, dcol2,dcol3 = st.beta_columns(3)
                dcol1.altair_chart(utils.graph_timeseries(sold_df, user_input))

                #st.markdown("Filtered Graph:")
                if len(domain_input1) > 0 and len(domain_input2) > 0:
                    dcol1.altair_chart(utils.graph_timeseries_domain(sold_df, domain_input1, domain_input2, user_input))

        else: #shows only unsold listings
            st.success("Data Retrieved!")

            first_listing_link = list(unsold_df['Link'])[0]
            utils.display_picture(first_listing_link, 500, 400, False)

            st.subheader("Dataframe:")
            st.write(unsold_df)
            if df_check_boxes[0]:
                latest_iteration.markdown('Getting pictures and summarized df... (this may take awhile so go ahead and get a second snack :cookie:)')
                unsold_df['final_price'] = utils.fix_new_price(unsold_df['sold_price'], unsold_df['new_price'], unsold_df['is_sold'], unsold_df['og_price'])
                filtered_df = unsold[['title', 'final_price', 'image_links']]
                st.write(filtered_df.to_html(escape=False), unsafe_allow_html=True)

            st.markdown(utils.get_table_download_link(unsold_df, user_input), unsafe_allow_html=True)

            if df_check_boxes[1]:
                dcol1, dcol2,dcol3 = st.beta_columns(3)
                dcol1.altair_chart(utils.graph_timeseries(unsold_df, user_input))

                st.markdown("Filtered Graph:")
                if len(domain_input1) > 0 and len(domain_input2) > 0:
                    dcol1.altair_chart(utils.graph_timeseries_domain(unsold_df, domain_input1, domain_input2, user_input))
