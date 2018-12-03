# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 14:37:54 2018

@author: Jack Biscupski
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from textwrap import wrap
from matplotlib.ticker import MaxNLocator


categories = dict()
features = dict()
df = pd.read_csv("Requests-Everything.csv")


firstDate = df.loc[0]['Created']
lastDate = df.loc[len(df)-1]['Created']
# extracting product types and their frequencies
for i in range(len(df)):
    x = str(df.loc[i]['Product']).split(',')
    f = str(df.loc[i]['Feature']).split(',')
    for y in x:
        # the case that the product is in neither the categories or features dict
        if y not in categories and y not in features and y != 'nan':
            categories[y] = 1
            features[y] = dict()
            # Since there are so many features that fall under SL: Response and SL: Content Fidelity
            # they are all grouped into one bigger parent category. This cuts down on the number of
            # labels needed for the graphs
            for fea in f:
                if fea.startswith('SL: Response'):
                    features[y]['SL: Response'] = 1
                elif fea.startswith('SL: Content Fidelity'):
                    features[y]['SL: Content Fidelity'] = 1
                else:
                    features[y][fea] = 1
        # the case that the product is in categories AND features dict - we can say
        # this is the only other case because of the way categories and features
        # dictionaries are added to (same product will be added to both at the same
        # time)
        elif y != 'nan':
            categories[y] += 1
            for fea in f:
                if fea not in features[y]:
                    if fea.startswith('SL: Response'):
                        features[y]['SL: Response'] = 1
                    elif fea.startswith('SL: Content Fidelity'):
                        features[y]['SL: Content Fidelity'] = 1
                    else:
                        features[y][fea] = 1
                else:
                    if fea.startswith('SL: Response'):
                        features[y]['SL: Response'] += 1
                    elif fea.startswith('SL: Content Fidelity'):
                        features[y]['SL: Content Fidelity'] += 1
                    else:
                        features[y][fea] += 1
          

i = 1
cmap = plt.get_cmap("gist_ncar") # set colormap for product pie chart

for k in features.keys():
    # create a new figure for each product, and set y axis such that only integers are used for ticks
    plt.figure(i).gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    i += 1    
    # get the necessary spacing of bins
    spaces = np.arange(len(features[k].keys()))
    # Create a bar chart for every individual product
    plt.bar(spaces, [int(v) for v in features[k].values()])
    labels = [s for s in features[k].keys()]
    
    # change font size and wrapping of x label ticks based on how many there are.
    # The more labels there are, the more crowded the bottom of the graph gets
    if len(spaces) > 11:
        # wrap takes (text, width)
        labels = ['\n'.join(wrap(l, 10)) for l in labels]
        plt.xticks(spaces, labels, fontsize=7)
    else:
        labels = ['\n'.join(wrap(l, 20)) for l in labels]
        plt.xticks(spaces, labels, fontsize=9)
    plt.title('Feature Requests for Product: "{0}" \n{1} to {2}\n'.format(k, firstDate, lastDate))
    
    

    

# simple pie chart showing each product type request and it's percentage of chart
plt.figure(i+1)
colors = cmap(np.linspace(0.1, 1.1, len(categories.keys())))
plt.pie([int(v) for v in categories.values()], labels=[s for s in categories.keys()], autopct='%1.1f%%', radius=1, colors=colors, shadow=True, startangle=90)
plt.title("Product Requests \n{0} to {1}\n".format(firstDate, lastDate))
plt.axis('equal')    

plt.figure(i+2)
vals = categories.values()
spaces = np.arange(len(vals))
plt.bar(spaces, [int(v) for v in vals])
labels = [s for s in categories.keys()]
plt.xticks(spaces, labels, fontsize=10)
plt.title("Total Feature Requests for Each Product from \n{0} to {1}\n".format(firstDate, lastDate))
    
      
# Things to work on:
# Put all SL: Content Fidelity and SL: Response into one cateogory - DONE    
# Convert stuff to bar charts and see if that looks better - DONE
# High level view: simple chart showing number of feature requests per product - DONE
# Name of file should indicate what it is    
    