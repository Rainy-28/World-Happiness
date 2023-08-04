import streamlit as st

from streamlit_option_menu import option_menu
import pandas as pd
import time
from annotated_text import annotated_text
import plotly.express as px
import json
import requests
from streamlit_lottie import st_lottie
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import numpy as np


st.set_page_config(layout="wide")

# sidebar menu
with st.sidebar: 
	selected = option_menu(
		menu_title = 'Navigation Pane',
		options = ['Abstract', 'Background Information', 'Data Cleaning', 
		'Familiarizing with Data','Exploratory Analysis','Data Analysis', 'Conclusion', 'Bibliography'],
		menu_icon = 'arrow-down-right-circle-fill',
		icons = ['bookmark-check', 'book', 'box', 'map', 'boxes', 'bar-chart', 
		'check2-circle','blockquote-left'],
		default_index = 0,
		)

if selected == 'Abstract':
	st.title('Abstract')

	def load_lottieurl(url: str):
		r = requests.get(url)
		if r.status_code != 200:
			return None
		return r.json()
	lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_u8jppxsl.json")
	st_lottie(
		lottie_coding,
		speed=1,
		reverse=False,
		loop=True,
		quality="low", # medium ; high
		height=None,
		width=300,
		key=None,
		)

	st.markdown('The World Happiness Report is a landmark survey of the state of global happiness. Nowadays, the increase in global recognition of the report is gaining new momentum, as happiness indicators are being widely applied across governments, companies and organizations to inform their policy-making decisions. These measurements of how happy citizens perceive themselves to be are proven to be effective in evaluating the progress of countries and regions.')
	st.markdown('In this case study, we will closely examine the data collected from the report and assess the difference between the national average of happiness scores in different countries, analyze the growth of happiness predictors over time as well as interpret the potential factors that affected the results. In addition, a prediction model will be constructed as a reference to future happiness values.')
	st.markdown('')
	st.markdown('')
	st.markdown('')
	st.markdown('')
	st.caption('Made by Selina Qiu')

if selected == 'Background Information':
	st.title('Background Information')
	st.caption('The following introduction is an excerpt from the World Happiness Report official website, to view their full documentation, visit the site https://worldhappiness.report/')
	st.markdown('The year 2022 marks the 10th anniversary of the World Happiness Report, which uses global survey data to report how people evaluate their own lives in more than 150 countries worldwide. The World Happiness Report 2022 reveals a bright light in dark times. The pandemic brought not only pain and suffering but also an increase in social support and benevolence. As we battle the ills of disease and war, it is essential to remember the universal desire for happiness and the capacity of individuals to rally to each other’s support in times of great need.')
	st.markdown('The World Happiness Report, and much of the growing international interest in happiness,  exists thanks to Bhutan. They sponsored Resolution 65/309, "Happiness: Towards a holistic approach to development," adopted by the General Assembly of the United Nations on 19 July 2011, inviting national governments to \"give more importance to happiness and well-being in determining how to achieve and measure social and economic development.\"')
	st.markdown('On 2 April 2012, chaired by Prime Minister Jigmi Y. Thinley and Jeffrey D. Sachs, the first World Happiness Report was presented to review evidence from the emerging science of happiness for the \'Defining a New Economic Paradigm: The Report of the High-Level Meeting on Well-being and Happiness.\' On 28 June 2012, the United Nations General Assembly adopted Resolution 66/281, proclaiming 20 March International Day of Happiness to be observed annually. The World Happiness Report is now released every year around March 20th as part of the International Day of Happiness celebration.')
	st.markdown('''### Original Datasets''')
	st.markdown('This main dataset consists of data collected on various different attributes of world happiness from 2005 to 2020. It contains 1948 rows and 11 columns, including the country name, year, and allotted statistics. Notice that there are some null values from certain countries in certain years.')
	st.caption('Click on the expand key to zoom in')
	happiness = pd.read_csv('world-happiness-report.csv')
	st.write(happiness)
	st.markdown('This second dataset is based on a similar report on world happiness in 2021. It has 20 columns and more predictors than the previous dataset, some of these variables will be later dropped in the data cleaning stage in order for the two tables to merge effectively.')
	st.caption('Click on the expand key to zoom in')
	happiness_2021 = pd.read_csv('world-happiness-report-2021.csv')
	st.write(happiness_2021)
	st.markdown('But before we conduct any analytical operations, we need to clean the data to ensure that our analysis is holistic and accurate.')

if selected == 'Data Cleaning':
	st.title('Data Cleaning')
	st.markdown('In this process, the two datasets will be combined into one complete table to conduct analysis. In order to achieve this, incorrectly formatted data will be fixed and irrelevant data will be removed. Through this process, the data is ensured to be correct, consistent, and usable.')
	annotated_text('Firstly, excessive columns that the two datasets do not share in common such as',("Positive affect", '', "#F0F3F4  "),'and ',("Negative affect", '', "#F0F3F4  "),'are dropped.')
	code = '''happiness_revised = happiness.loc[happiness['Country name'].isin(happiness_2021['Country name'])].copy()
happiness_revised.drop(['Positive affect','Negative affect'],axis = 1,inplace=True)'''
	st.code(code, language = 'python')
	st.markdown('Notice that though the two datasets share many columns that measure the same variables, the naming of the columns is different. So then some columns of the 2021 dataset are renamed to match the main dataset in order to successfully combine the two later.')
	code2 = '''happiness_2021.rename({'Ladder score':'Life Ladder',
                       'Logged GDP per capita':'Log GDP per capita',
                       'Healthy life expectancy':'Healthy life expectancy at birth'},
                       axis=1,inplace=True)'''
	st.code(code2, language = 'python')
	annotated_text('In the 2021 dataset the column',("year", '', "#F0F3F4  "),'is not present. So a year column is added and assigned to 2021 for it to combine with the main dataset.')
	code3 = '''happiness_2021['year'] = 2021
happiness_2021 = happiness_2021[list(happiness_revised.columns) + ['Regional indicator']]'''
	st.code(code3, language = 'python')
	st.markdown('After these arrangements, the revised datasets are concatenated to form one complete data table. However, it is not quite finished yet.')
	code4 = '''merged_table = pd.concat([happiness_revised,happiness_2021])'''
	st.code(code4, language = 'python')
	annotated_text('Last but not least, a region column is added so that analysis can be done in comparison of different regions. A ', ("Regional indicator", '', "#F0F3F4  "),'column can be found in the original 2021 dataset. The data in that column is used to create a dictionary that assigns each country with its region. The new column ', ("Region", '', "#F0F3F4  "),'is then made in the concatenated dataset using the dictionary to finally complete this process.')
	code5 = '''region_dict = {k:v for k,v in zip(happiness_2021['Country name'],happiness_2021['Regional indicator'])}
merged_table['Region'] = merged_table['Country name'].replace(region_dict)
merged_table.drop('Regional indicator',axis = 1,inplace = True)
merged_table'''
	st.code(code5, language = 'python')
	st.caption('Click on the expand key to zoom in')
	merged_table = pd.read_csv('world_happiness2.csv')
	st.write(merged_table)
	st.markdown('Since we have the cleaned and completed data, we can start by taking a closer look into it and getting to know it better.')

if selected == 'Familiarizing with Data':
	st.title('Familiarizing with Data')
	st.markdown('''### Representation of Regions''')
	st.markdown('The following sunburst chart helps visualize the proportion of representation from each region in the dataset. Bear in mind that the total number of countries from different regions varies. This chart provides a sense of which countries are included, and how much they contributed to the data.')
	st.caption('Click on any sector to focus on its attributed region and zoom in to get a closer look at the representation of the countries within. Click again on the center core of the plot to zoom back out.')
	merged_table = pd.read_csv('world_happiness2.csv')
	sunburst = px.sunburst(merged_table, path = ['Region', 'Country name'], values = 'Life Ladder', height = 800, )
	st.plotly_chart(sunburst)
	st.markdown('''### Columns Description''')
	st.markdown('Understanding each of the variables that the data is measuring is also crucial to analysis.')
	st.caption('Click on the expand key to zoom in')
	merged_table = pd.read_csv('world_happiness2.csv')
	st.write(merged_table)
	annotated_text(("Country name", '', "#F0F3F4  "),": name of the country")
	annotated_text('')
	annotated_text(("year", '', "#F0F3F4  "),": the year during which the data was collected")
	annotated_text('')
	annotated_text(("Life Ladder", '', "#F0F3F4  "),": the national average of responses to the self-evaluation of the status of the respondent's life on a “ladder” scale ranging from 0 to 10, where 0 means the worst possible life and 10 the best possible life.")
	st.caption('Drag the slider to assess your own "life ladder" value')
	ll = st.slider('Evaluate your current life status: 0 being the worst possible life, 10 being the best possible life', value = 5, min_value = 0, max_value = 10, step = 1)
	st.write('Life ladder:', ll)
	annotated_text('')
	annotated_text(("Log GDP per capita", '', "#F0F3F4  "),": the result of taking the natural log of the Gross Domestic Product per person on a national scale")
	annotated_text('')
	annotated_text(("Social support", '', "#F0F3F4  "),": the national average of the binary responses (either 0 or 1) to the Gallup World Poll (GWP) question “If you were in trouble, do you have relatives or friends you can count on to help you whenever you need them, or not?”")
	st.caption('Drag the slider to assess your own "social support" value')
	ss = st.slider('If you were in trouble, do you have relatives or friends you can count on to help you: 0 being no, 1 being yes', value = 0, min_value = 0, max_value = 1, step = 1)
	st.write('Social support:', ss)
	annotated_text('')
	annotated_text(("Healthy life expectancy at birth", '', "#F0F3F4  "),":  the average number of years that a person can expect to live in full health by taking into account years lived in less than full health due to disease and/or injury.")
	annotated_text('')
	annotated_text(("Freedom to make life choices", '', "#F0F3F4  "),": the national average of binary responses to the GWP question “Are you satisfied or dissatisfied with your freedom to choose what you do with your life?”")
	st.caption('Drag the slider to assess your own "freedom to make life choices" value')
	fc = st.slider('Are you satisfied or dissatisfied with your freedom to choose what you do with your life: 0 being dissatisfied, 1 being satisfied', value = 0, min_value = 0, max_value = 1, step = 1)
	st.write('Freedom to make life choices:', fc)
	annotated_text('')
	annotated_text(("Generosity", '', "#F0F3F4  "),": the residual of regressing the national average of GWP responses to the question “Have you donated money to a charity in the past month?” on GDP per capita.")
	annotated_text('')
	annotated_text(("Perceptions of corruption", '', "#F0F3F4  "),": the average of binary answers to two GWP questions: “Is corruption widespread throughout the government or not?” and “Is corruption widespread within businesses or not?” Where data for government corruption are missing, the perception of business corruption is used as the overall corruption-perception measure.")
	st.caption('Drag the sliders to assess your own "perceptions of corruption" value')
	pc1 = st.slider('Is corruption widespread throughout the government: 0 being no, 1 being yes', value = 0, min_value = 0, max_value = 1, step = 1)
	pc2 = st.slider('Is corruption widespread within businesses: 0 being no, 1 being yes', value = 0, min_value = 0, max_value = 1, step = 1)
	st.write('Perceptions of corruption:', (pc1+pc2)/2)
	annotated_text('')
	annotated_text(("Region", '', "#F0F3F4  "),": the region to which the country belongs to")
	st.markdown('')
	st.markdown('')
	st.markdown('Now that we have a more concrete understanding of the data, we can start conducting analysis.')
	

if selected == 'Exploratory Analysis':
	st.title('Exploratory Analysis')
	st.subheader('With Pandas Profiling')
	merged_table = pd.read_csv('world_happiness2.csv')
	profile = ProfileReport(merged_table)
	st_profile_report(profile)


if selected == 'Data Analysis':
	
	st.title('Data Analysis')
	st.header('Regional Difference')
	st.markdown('Throughout history, it is known that countries that are adjacent to one another or are in the same geographical region are likely to have similar circumstances in many aspects. This is also true in happiness scores. Through the different visualizations, it is observed that countries of separate regions are probable to have incompatible values.')
	col1,col2 = st.columns([4,5])
	col1.subheader('Scatter comparison between countries by region')
	roption = col1.selectbox(
     'Select the region you would like to evaluate',
     ('Central and Eastern Europe','Commonwealth of Independent States', 'South Asia',
       'Middle East and North Africa', 'Latin America and Caribbean', 'North America and ANZ',
       'Western Europe', 'Sub-Saharan Africa', 'Southeast Asia',
       'East Asia'))
	hfoption = col1.selectbox(
     'Select the happiness factor you would like to evaluate',
     ('Healthy life expectancy at birth', 'Life Ladder',
       'Social support', 'Generosity',
       'Log GDP per capita', 'Perceptions of corruption',
       'Freedom to make life choices'))
	merged_table = pd.read_csv('world_happiness2.csv')
	col2.plotly_chart(px.scatter(merged_table.loc[merged_table['Region']== roption], y = hfoption, color = 'Country name', x= 'year',
		size = 'year', size_max = 12))
	col1.markdown('This scatter plot visualizes the happiness values of countries sorted in the regions to which they belong. Notice how the y-axis scale changes according to the region selected, this difference shows the variation of happiness levels across different regions.')
	col1.markdown('')
	col1.markdown('')
	col1.subheader('Scatter comparison between regions - Global')
	hf1option = col1.selectbox(
     'Select the first happiness factor you would like to evaluate',
     ('Healthy life expectancy at birth', 'Life Ladder',
       'Social support', 'Generosity',
       'Log GDP per capita', 'Perceptions of corruption',
       'Freedom to make life choices'))
	hf2option = col1.selectbox(
     'Select the second happiness factor you would like to evaluate',
     ( 'Life Ladder','Healthy life expectancy at birth',
       'Social support', 'Generosity',
       'Log GDP per capita', 'Perceptions of corruption',
       'Freedom to make life choices'))
	foption = col1.selectbox(
     'Select the format of display: by regional average or individual countries',
     ('Region','Country name'))
	col1.caption('Press the play button to view animation')

	if hf1option == 'Healthy life expectancy at birth':
		x_range = [0,80]
	elif hf1option == 'Life Ladder':
		x_range = [0,10]
	elif hf1option == 'Social support':
		x_range = [0,1]
	elif hf1option == 'Generosity':
		x_range = [-0.5,1]
	elif hf1option == 'Log GDP per capita':
		x_range = [6,12]
	elif hf1option == 'Perceptions of corruption':
		x_range = [0,1]
	elif hf1option == 'Freedom to make life choices':
		x_range = [0,1]
	else:
		x_range = None

	if hf2option == 'Healthy life expectancy at birth':
		y_range = [0,80]
	elif hf2option == 'Life Ladder':
		y_range = [0,10]
	elif hf2option == 'Social support':
		y_range = [0,1]
	elif hf2option == 'Generosity':
		y_range = [-0.5,1]
	elif hf2option == 'Log GDP per capita':
		y_range = [6,12]
	elif hf2option == 'Perceptions of corruption':
		y_range = [0,1]
	elif hf2option == 'Freedom to make life choices':
		y_range = [0,1]
	else:
		y_range = None


	
	ani_data = pd.read_csv('animation_frame1')
	col2.plotly_chart(px.scatter(ani_data, x= hf1option, y= hf2option, 
           animation_frame="year", animation_group= foption ,category_orders = {'year':np.arange(2005, 2022)},
           color="Region", hover_name="Country name", size = 'year', range_x = x_range, range_y = y_range,
           size_max=12, width = 800, height = 500))
	st.markdown('')
	st.markdown('')
	st.markdown('')
	st.markdown('')
	st.subheader('Box plot - life ladder comparison by region')
	
	st.markdown('Through this box and whiskers plot visualization, outliers that are out of the upper and lower fence ranges of their regions are represented as individual dots and are easily identified. Such as Afghanistan, the hover data displays that it has a life ladder of 2.375, whereas the lower fence of its allotted region -South Asia- is 3.131. Other than identifying outliers, this plot also helps us to visualize and compare the average as well as the range of values of different regions. It is easily observed that North America and ANZ and Western Europe are concentrated at a relatively high ladder score, on the other hand, South Asia and Sub-Saharan Africa have the lowest span.')
	st.plotly_chart(px.box(merged_table, x = 'Region', y = 'Life Ladder', hover_name = 'Country name', color = 'Region', color_discrete_sequence = px.colors.qualitative.Light24, width = 1100, height = 500))
	st.markdown('')
	st.markdown('')
	st.markdown('')
	col3,col4 = st.columns([4,5])
	col3.subheader('Choropleth map visualization')
	hp3option = col3.selectbox('Select the happiness factor you would like to evaluate',
		( 'Life Ladder','Healthy life expectancy at birth',
			'Social support', 'Generosity',
			'Log GDP per capita', 'Perceptions of corruption',
			'Freedom to make life choices'))
	col3.caption('Press the play button to view animation')
	col3.caption('Click and drag the choropleth to rotate the globe')
	col3.caption('Hover over a colored area to view the country name and its specific allotted values.')
	col4.plotly_chart(px.choropleth(merged_table, locations = 'Country name', locationmode = 'country names', 
              color = hp3option, animation_frame = 'year', 
              category_orders = {'year':np.arange(2005, 2022)}
             ,projection = 'orthographic', color_continuous_scale = px.colors.sequential.RdBu, height = 600,
             hover_name = 'Country name'))



	col5,col6 = st.columns([4,5])
	col5.markdown('### Three-Dimensional Scatter Plot')
	col5.markdown('This scatter plot shows the relation between values from 3 axes: \'Life Ladder\', \'Log GDP per capita\' and \'Generosity\', with each dot representing one country and its happiness status in the year 2021. The colors are attributed according to the country\'s region, helping visualize and differentiate the distribution of happiness levels in various regions.')
	col5.caption('Click and drag the scatter plot to rotate and change orientation.')
	col5.caption('Hover over a dot to view the country name and its specific allotted values.')
	col6.plotly_chart(px.scatter_3d(merged_table.loc[merged_table['year']== 2021], x = 'Life Ladder', y = 'Generosity', z = 'Log GDP per capita',  size_max = 5,
              color = 'Region', height = 600, width = 800, hover_name = 'Country name'))
	st.markdown('Through these visualizations, it is easily observed that there are trends in happiness factors of the countries from the same region. The statistics show that the happiness values of the regions Western Europe and especially North America and ANZ have a more compact structure - in other words the range of varying values for those two regions is relatively small (as seen on the box plot) and has a high average score compared with other regions that are represented in the data. For there to be a high happiness score, the region\'s economy is a key contributing factor. Looking closer, it is recognized that countries of Western Europe are rich in agricultural and industrial diversity, generally have more developed economies, and obtain a high level of income per capita. Moreover, North America, Australia, and New Zealand are all developed countries. So it is easily justifiable for those regions to obtain high happiness levels. On the other hand, the values of South Asia and South-Saharan Africa are concentrated at a comparatively low span. This might be because these two regions mainly consist of developing countries, and the latter has the world\'s lowest total GDP.')
	st.header('Predictors progression')
	st.subheader('Line chart - growth of happiness factors over time')

	optionn = st.selectbox(
     'Select the happiness factor you would like to evaluate',
     ('Life Ladder','Healthy life expectancy at birth',
       'Social support', 'Freedom to make life choices', 'Generosity',
       'Log GDP per capita', 'Perceptions of corruption'))


	col7, col8 = st.columns([10,15])
	regional = []
	col7.caption('Check the boxes to display allotted data')
	sa = col7.checkbox('South Asia')
	cee = col7.checkbox('Central and Eastern Europe', value = True)
	mena = col7.checkbox('Middle East and North Africa')
	lac = col7.checkbox('Latin America and Caribbean')
	cis = col7.checkbox('Commonwealth of Independent States')
	naa = col7.checkbox('North America and ANZ')
	we = col7.checkbox('Western Europe')
	ssa = col7.checkbox('Sub-Saharan Africa')
	sea = col7.checkbox('Southeast Asia')
	ea = col7.checkbox('East Asia')
	if sa: 
		regional.append('South Asia')
	if cee: 
		regional.append('Central and Eastern Europe')
	if mena: 
		regional.append('Middle East and North Africa')
	if lac: 
		regional.append('Latin America and Caribbean')
	if cis: 
		regional.append('Commonwealth of Independent States')
	if naa: 
		regional.append('North America and ANZ')
	if we: 
		regional.append('Western Europe')
	if ssa: 
		regional.append('Sub-Saharan Africa')
	if sea: 
		regional.append('Southeast Asia')
	if ea: 
		regional.append('East Asia')
	check_data = merged_table.loc[merged_table['Region'].isin(regional)]
	#col8.plotly_chart(px.line(check_data, y = optionn, color = 'Country name', x= 'year', height = 500))
	col8.plotly_chart(px.line(check_data, y = optionn, color = 'Country name', x= 'year', height = 500))
	st.markdown('In this graph, you can choose to visualize the progression of any happiness factor in the data set. In the textual analysis, however, we will focus on three major happiness factors and their trends over the years. Other than observing the growth of happiness factors over time, we will also investigate the reasons behind sudden changes to the trendlines, and associate them with political, environmental, or economical shifts in that allotted time period that are potentially responsible for the shifts.')
	st.markdown('###### Life Ladder')
	st.markdown('The Life Ladder is the average value of citizens\' self-evaluation of their current status in life. Through the line graph, we can see that the life ladder of each country has many drops and rises throughout the years in no particular global pattern. However, it still can be seen that the general trend is that the life ladder values are growing over time.')
	st.markdown('###### Healthy life expectancy at birth')
	st.markdown('On the other hand, the healthy life expectancy at birth has relatively stable growth and has a much more obvious trend. We can see that - using the visualization - the healthy life expectancy has been increasing fairly steadily over the years, with no disruption to the rising pattern except for the year 2021, during which all the countries seems to have taken a dip in their values. With the coronavirus, pandemic stretching on for the second year along with the emergence of new variants, and as the restrictions continue to be imposed upon citizens, professionals claim that the year brought on a "new low" in people\'s mental health globally. Not only have people exposed to the risk of contracting the deadly virus which can severely damage health and major organs permanently, but the added depression among citizens also lowers the life expectancy on a global level. Studies find that poor mental health can lead to a decrease in longevity. ')
	st.markdown('###### Log GDP per capita')
	st.markdown('Similarly to healthy life expectancy at birth, log GDP per capita has a steady trendline with general upward growth. One disruption to the trend is the year 2020, in which the majority of countries had a decrease in their GDP value but recovered some growth in the following year. The cause of that is likely to be the COVID-19 recession (a global economic recession due to the pandemic breakout), which started in most countries in early February 2020. The pandemic significantly slowed consumer activity. Other than that, the 2020 stock market crash was also a major factor that contributed to the recession in economic growth. And precautions that the governments took against it - such as the lockdown, limit in numbers in public spaces, etc. - rapidly increased unemployment and product prices.')
	st.markdown('')
	st.markdown('')
	st.markdown('')
	st.subheader('Linear Regression Prediction Model')
	col9,col10 = st.columns(2)
	year_num = col9.number_input('Insert the year you would like to predict/check for', value = 2022, min_value = 2005, max_value = 2100)
	country_option = col10.selectbox('Select the country you would like to evaluate', (merged_table['Country name'].unique()))
	optionn2 = st.selectbox(
     'Select the happiness factor you would like to evaluate',
     ('Log GDP per capita','Healthy life expectancy at birth',
       'Social support', 'Life Ladder', 'Freedom to make life choices', 'Generosity', 'Perceptions of corruption'))
	fig = px.scatter(merged_table.loc[merged_table['Country name'] == country_option], y = optionn2,
           x= 'year',  trendline="ols", trendline_options=dict(log_x=True), color = 'Country name', color_discrete_sequence = ['#6495ED'],trendline_color_override="red", width = 960)
	###### the following doesnt work
	results = px.get_trendline_results(fig)
	model = results.px_fit_results[0]
	pred_x = np.array([1,np.log10(year_num)])
	pred_y = model.predict(pred_x)
	button = st.button('Return Result')
	if button : 
		annotated_text(f'〚Predicted {optionn2} in {year_num} for {country_option}:',(f'{pred_y[0]:.2f}', '', "#F0F3F4  "),'〛')
		st.plotly_chart(fig)
	else: 
		st.caption('Click to return data prediction when variables are inputted')
	# dont know what to put in the first ()       results.query("x == year_num").px_fit_results.iloc[0].summary()

	

	### explanation




if selected == 'Conclusion':
	st.title('Conclusion')
	def load_lottieurl(url: str):
		r = requests.get(url)
		if r.status_code != 200:
			return None
		return r.json()
	lottie_coding = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_qp1q7mct.json")
	st_lottie(
		lottie_coding,
		speed=1,
		reverse=False,
		loop=True,
		quality="low", # medium ; high
		height=None,
		width=600,
		key=None,
		)
	st.markdown('As the society progresses onwards with the constant development of technological advancements, the environment, privileges, and infrastructures available for citizens and the overall standard of living are also gradually rising. Through the analysis of the data, we can see that most of the happiness factors have an increasing trend in proportion to time on a global level. Though the recent pandemic has caused some degree of decline in the originally rising pattern, it does not make a significant impact on the general trend. And in the foreseeable future, it is speculated that the drop in happiness score will recover.')

if selected == 'Bibliography':
	st.title('Referenced Sources')
	st.markdown('##### Original Datasets')
	st.markdown('- “Read the Reports.” Read the Reports, https://worldhappiness.report/archive/')
	st.markdown('- Singh, Ajaypal. “World Happiness Report 2021.” Kaggle, 22 Mar. 2021, https://www.kaggle.com/datasets/ajaypalsinghlo/world-happiness-report-2021')
	st.markdown('##### Other Resources')
	st.markdown('- “Changing World Happiness.” Changing World Happiness, https://worldhappiness.report/ed/2019/changing-world-happiness/')
