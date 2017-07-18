# Veggie network


In [this article](http://www.nature.com/articles/doi:10.1038%2Fsrep00196)
an [ingredient network](https://github.com/rgarcia-herrera/furry-spoon/blob/master/data/get_data.sh) was
created for an omnivorous diet.

What differences are there in the structure of omnivorous, vegetarian
and vegan ingredient networks?

Three categories are used to classify ingredientes:
 - carnic, ingredients are the flesh of animals
 - animal origin, such as milk and honey
 - vegan, just plants and fungi

The omnivorous network is constructed from 56,502 recipes from all
over the world. Nodes are ingredients and amount to 381, out of which
55 are carnic, 33 have animal origin and 293 are vegan.

<img src="https://raw.githubusercontent.com/rgarcia-herrera/furry-spoon/master/plots/ingredients_3cat.png" width="600px">
Hiveplot constructed from the omnivorous network

## Axes

There are two axes for each category, both the same size, for the
purpose of displaying intercategory edges. Khaki axes are for
ingredients of animal origin, green axes for vegan ingredients and red
axes for carnic ingredients. Axis length is proportional to ingredient
count per category.

## Nodes and edges

Nodes on the axes are sorted by connectivity degree, descending
outwards from the center of the hiveplot.

Colors of edges in same category:
 - Red lines connect carnic to carnic.
 - Green lines connect vegan to vegan.
 - Brown lines connect animal origin to animal origin. 
 
Colors of edges across different categories:
 - Purple lines connect ingredients of animal origin to carnic
   ingredients. 
 - Pale brown lines connect ingredients of animal origin to vegan
   ingredients.
 - Yellow lines connect vegan to carnic ingredients.

