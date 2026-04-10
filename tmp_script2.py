import os
import re

base_dir = r'c:\Users\siyaa\OneDrive\Documents\cicada\CICADA\app\templates'
index_path = os.path.join(base_dir, 'index.html')
product_path = os.path.join(base_dir, 'product.html')
contact_path = os.path.join(base_dir, 'contact.html')

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

nav_end = content.find('</nav>') + 6
footer_start = content.find('<footer id="footer"')

header = content[:nav_end]
footer = content[footer_start:]

contact_body = """
  <section id="contact-us" class="py-5 mt-5">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-md-6 mb-5">
          <h2 class="section-title mb-4" style="color: #4A3320; font-family: 'Marcellus', serif; font-size: 3rem;">Get in Touch</h2>
          <p class="mb-5" style="color: #5C4A3D; font-size: 1.1rem; line-height: 1.8;">
            We would love to hear from you. Whether you have a question about a product, need styling advice, or simply want to share your experience with CICADA RISE, we are here for you.
          </p>
          <div class="d-flex align-items-center mb-4">
            <div style="width: 50px; height: 50px; border-radius: 50%; background-color: #f7f3e8; display: flex; align-items: center; justify-content: center; margin-right: 20px;">
                <svg width="24" height="24" viewBox="0 0 24 24" style="color: #C0A848;"><use xlink:href="#user"></use></svg>
            </div>
            <div>
              <h5 style="color: #4A3320; margin-bottom: 2px;">Visit Our Studio</h5>
              <p style="color: #8f8f8f; margin-bottom: 0;">Experience the premium quality in person.</p>
            </div>
          </div>
          <div class="d-flex align-items-center mb-4">
            <div style="width: 50px; height: 50px; border-radius: 50%; background-color: #f7f3e8; display: flex; align-items: center; justify-content: center; margin-right: 20px;">
                <svg width="24" height="24" viewBox="0 0 24 24" style="color: #C0A848;"><use xlink:href="#check"></use></svg>
            </div>
            <div>
              <h5 style="color: #4A3320; margin-bottom: 2px;">Email Us</h5>
              <p style="color: #8f8f8f; margin-bottom: 0;">care@cicadarise.com</p>
            </div>
          </div>
          <div class="d-flex align-items-center">
            <div style="width: 50px; height: 50px; border-radius: 50%; background-color: #f7f3e8; display: flex; align-items: center; justify-content: center; margin-right: 20px;">
                <svg width="24" height="24" viewBox="0 0 24 24" style="color: #C0A848;"><use xlink:href="#arrow-cycle"></use></svg>
            </div>
            <div>
              <h5 style="color: #4A3320; margin-bottom: 2px;">Call Us</h5>
              <p style="color: #8f8f8f; margin-bottom: 0;">+91 8086273188</p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="p-5" style="background-color: #fff; box-shadow: 0 10px 40px rgba(0,0,0,0.05); border-radius: 10px;">
            <h3 class="mb-4" style="color: #4A3320; font-family: 'Marcellus', serif;">Send a Message</h3>
            
            {% if messages %}
            <div class="messages mb-4">
                {% for message in messages %}
                <div class="alert {% if message.tags %}alert-{{ message.tags }}{% endif %} alert-dismissible fade show" role="alert" style="background-color: #f7f3e8; border-color: #C0A848; color: #4A3320;">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                {% endfor %}
            </div>
            {% endif %}

            <form method="POST" action="{% url 'contact' %}">
              {% csrf_token %}
              <div class="mb-4">
                <input type="text" class="form-control form-control-lg border-0 border-bottom" id="name" name="name" placeholder="Your Name" required style="border-radius: 0; box-shadow: none; border-color: #e0e0e0;">
              </div>
              <div class="mb-4">
                <input type="email" class="form-control form-control-lg border-0 border-bottom" id="email" name="email" placeholder="Your Email" required style="border-radius: 0; box-shadow: none; border-color: #e0e0e0;">
              </div>
              <div class="mb-4">
                <input type="text" class="form-control form-control-lg border-0 border-bottom" id="subject" name="subject" placeholder="Subject" style="border-radius: 0; box-shadow: none; border-color: #e0e0e0;">
              </div>
              <div class="mb-4">
                <textarea class="form-control form-control-lg border-0 border-bottom" id="message" name="message" rows="4" placeholder="Your Message" required style="border-radius: 0; box-shadow: none; border-color: #e0e0e0; resize: none;"></textarea>
              </div>
              <button type="submit" class="btn btn-dark btn-lg text-uppercase w-100 py-3" style="background-color: #4A3320; border: none; letter-spacing: 2px;">Send Message</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

with open(contact_path, 'w', encoding='utf-8') as f:
    f.write(header + contact_body + footer)

def update_links(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            c = f.read()
        
        # Replace the navigation 'Contact' link to use the actual view. 
        # Since it might be href="#" and text "Contact"
        c = re.sub(r'href="#"([^>]*>Contact</a>)', r'href="{% url \'contact\' %}"\1', c)
        
        # Replace Footer "Contact" 
        c = re.sub(r'href="#"([^>]*>Contact</a>)', r'href="{% url \'contact\' %}"\1', c)
        c = re.sub(r'href="#"([^>]*>Contact Us</a>)', r'href="{% url \'contact\' %}"\1', c)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(c)
    except Exception as e:
        print(f"Error updating {filepath}: {e}")

update_links(index_path)
update_links(product_path)
# We might need to update contact_path as well to have proper links
update_links(contact_path)

print("contact.html created and links updated.")
