FROM prestashop/prestashop:1.7.7.8

COPY webshop/ ./
COPY ssl/ /etc/apache2/sites-available

RUN a2enmod ssl

EXPOSE 80
EXPOSE 443