from django.contrib.sitemaps import Sitemap
from products.models import Product

class ProductSitemap(Sitemap):
    changfreq = 'always'
    def products(self):
        return Product.objects.all()
