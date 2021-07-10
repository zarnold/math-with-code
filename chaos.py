"""This Module generate charts showing chaos emergence from simple iteration
"""

import pylab as plt
import seaborn as sns
import pandas as pd 
import numpy as np 

sns.set_context("paper")
sns.set_style("white")
myc = sns.color_palette("Paired", as_cmap=True)

# Currying
# We generate a serie generator from a parameter

def generator(mu=1) : 
    def xnplus1(xn):
        # Logistic equation. See https://fr.wikipedia.org/wiki/Suite_logistique
        return mu * xn * (1-xn)
    return xnplus1


# Generate the serie
def generate(mu,c=10000) : 
    gen = generator(mu)
    # Startign from one initial value
    seed = [0.01]
    #  Generate the serie
    for n in range(c):
        # growing the seed. Next term is generator applied on previous one
        seed = np.append(seed, gen(seed[-1]))
    data      = pd.DataFrame(data=seed, columns=['y']) 
    data['x'] = [i for i,v in enumerate(data["y"])]
    data['mu'] = mu
    return data 


# Get all the stationnary points ( or a good approximation ) for a given mu
# Same things thnt before but we get the set of value
# reached by the serie after a lot of generation
# Some oscillate between a couple of point
# Some others take an infinity of values ( chaotic regime )
def getwellpoint(mu,c=10000):
    print("Generating {}".format(mu))
    gen = generator(mu)
    seed = [0.01]
    #  Generate the serie
    for n in range(c):
        seed = np.append(seed, gen(seed[-1]))
    ## Assume the 100th last generation are stationnary
    wells = list(set(seed[-100:]))
    data      = pd.DataFrame(data=wells, columns=['well']) 
    data['mu'] = mu
    data['n'] = len(wells)
    return data



# Just charts parameters
# Do not go belong 4
maxv=4
sample=6

##################################################################### First, a discret stationnary point representation with few points
# Tips for generating more sample at the end
mu_value = (maxv+1-np.logspace(0, 2, num=sample**2, base=2))[::-1]
# round it
mu_value = (1000 * mu_value).round() / 1000

series=[]
for mu in mu_value:
    print("#" * 70)
    series.append(getwellpoint(mu))

# Put them all in a dataframe
data = pd.concat(series)


g = sns.relplot(data=data, x=0.5, y="well", col="mu", col_wrap=sample, alpha=.5,  s=80)
g.savefig("charts/stationnary_points.png")

########################################################################### Focus on transition region

mu_value =mu_value= np.linspace(3.4,3.8,sample**2)
# round it
mu_value = (1000 * mu_value).round() / 1000

series=[]
for mu in mu_value:
    print("#" * 70)
    series.append(getwellpoint(mu))

# Put them all in a dataframe
data = pd.concat(series)


g = sns.relplot(data=data, x=0.5, y="well", col="mu", col_wrap=sample, alpha=.5,  s=60)
g.savefig("charts/stationnary_points_focus.png")


########################################################################### Approaching feigen baum constant


mu_value =mu_value= np.linspace(3.55,3.59,sample**2)
# reduce Float precision
mu_value = (1000 * mu_value).round() / 1000

series=[]
for mu in mu_value:
    print("#" * 70)
    series.append(getwellpoint(mu))

# Put them all in a dataframe
data = pd.concat(series)


g = sns.relplot(data=data, x=0.5, y="well", col="mu", col_wrap=sample, alpha=.5,  s=60)
g.savefig("charts/stationnary_points_transition.png")


############################################################################# Feigenbaum tree
# Tips for generating more sample at the end
mu_value = (maxv+1-np.logspace(0, 2, num=800, base=2))[::-1]
# reduce Float precision
mu_value = (1000 * mu_value).round() / 1000


series=[]
for mu in mu_value:
    print("#" * 70)
    series.append(getwellpoint(mu))

# Put them all in a dataframe
data = pd.concat(series)




g = sns.relplot(data=data, x="mu", y="well",palette= myc, hue="n", s=1)
g.savefig("charts/feigenbaum.png")

