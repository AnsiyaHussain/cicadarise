import os

base_dir = r'c:\Users\siyaa\OneDrive\Documents\cicada\CICADA\app\templates'
index_path = os.path.join(base_dir, 'index.html')
product_path = os.path.join(base_dir, 'product.html')

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

nav_end = content.find('</nav>') + 6
footer_start = content.find('<footer id="footer"')

header = content[:nav_end]
footer = content[footer_start:]

product_body = '''
  <section id="product-details" class="py-5 mt-5">
    <div class="container">
      <div class="row">
        <div class="col-md-6 mb-4">
          <img src="{% static \'images/product-item-1.jpg\' %}" alt="Product Image" class="img-fluid rounded shadow-sm">
        </div>
        <div class="col-md-6">
          <h2 class="product-title mb-3" style="color: #4A3320; font-family: \'Marcellus\', serif;">Dark florish onepiece</h2>
          <h4 class="product-price mb-4" style="color: #C0A848;">$95.00</h4>
          <p class="product-description mb-4" style="color: #5C4A3D; font-size: 1.1rem; line-height: 1.6;">
            Curated for the modern wardrobe. Explore our premium collection of versatile, beautifully tailored styles designed to inspire confidence in every step.
          </p>
          <div class="mb-4">
            <h5 style="color: #4A3320;" class="mb-3">Select Size</h5>
            <div class="d-flex gap-2">
              <button class="btn btn-outline-dark px-4 py-2">S</button>
              <button class="btn btn-outline-dark px-4 py-2">M</button>
              <button class="btn btn-outline-dark px-4 py-2">L</button>
              <button class="btn btn-outline-dark px-4 py-2">XL</button>
            </div>
          </div>
          <div class="mb-4">
            <h5 style="color: #4A3320;" class="mb-3">Quantity</h5>
            <div class="d-flex align-items-center gap-3">
              <div class="input-group" style="width: 120px;">
                <button class="btn btn-outline-secondary" type="button">-</button>
                <input type="text" class="form-control text-center" value="1">
                <button class="btn btn-outline-secondary" type="button">+</button>
              </div>
            </div>
          </div>
          <a href="#" class="btn btn-dark btn-lg text-uppercase w-100 py-3 mb-3" style="background-color: #4A3320; border: none;">Add to Cart</a>
          <div class="d-flex align-items-center gap-2 mt-4" style="color: #8f8f8f; font-size: 0.9rem;">
            <svg width="24" height="24" viewBox="0 0 24 24"><use xlink:href="#shopping-bag"></use></svg>
            <span>Complimentary shipping on orders over $150.</span>
          </div>
          <div class="d-flex align-items-center gap-2 mt-2" style="color: #8f8f8f; font-size: 0.9rem;">
            <svg width="24" height="24" viewBox="0 0 24 24"><use xlink:href="#arrow-cycle"></use></svg>
            <span>Effortless returns within 14 days.</span>
          </div>
        </div>
      </div>
    </div>
  </section>
'''

with open(product_path, 'w', encoding='utf-8') as f:
    f.write(header + product_body + footer)

# Also update the links in index.html to point to product view
# Only replace 'href="index.html"' inside the product scope or generally the ones that look like product links
# Actually, the user said "click the link", maybe we can just replace 'href="index.html"' with 'href="{% url \'product\' %}"' for the image links
content = content.replace('href="index.html"', 'href="{% url \'product\' %}"')
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("done")
