
## CONTENT FILTERING:
Per product moet er 4 recommendations gedaan worden voor soortgelijke producten.
  Dit betekent als ik een product kies met sub-sub-category_A, waarvan bekend is dat het een product voor vrouwen is,
  dat ik vervolgens andere vrouwen producten verkrijg binnen het sub_sub_category, maar wel anders dan sub_sub_category_A, als recommendation.

## COLLABORATIVE FILTERING:
Per product moet er 4 recommendations gedaan worden voor producten die vaker samen voorkomen in een bestelling.
  Dit houdt in dat eerst gechecked wordt in welke sessie een product voorkomt, en welke andere producten daarbij samen
  gekocht worden. Vervolgens worden de daarbij samen gekochte producten opgeteld om te zien hoevaak de desbetreffende producten
  voorkomen. Dit wordt vervolgens overwogen en de producten met het meest voorkomend aantal, van hoog naar laag gesorteerd,
  wordt opgeslagen in de recommendation kolom.

