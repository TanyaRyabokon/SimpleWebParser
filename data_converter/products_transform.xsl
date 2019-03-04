<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml"
            encoding="UTF-16"
            doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"
            doctype-public="-//W3C//DTD XHTML 1.1//EN" indent="yes"/>
  <xsl:template match="/">
    <html>
      <head>
        <title>Products</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous" />
      </head>
      <body>
        <h1 align="center" class="display-3">Products</h1>
        <table style="width: 90%" class="table table-hover mx-auto">
            <thead>
                <tr>
                    <th scope="col" align="center">Image</th>
                    <th scope="col" align="center">Description</th>
                    <th scope="col" align="center">Price</th>
                </tr>
            </thead>
            <tbody>
                <xsl:apply-templates/>
            </tbody>
        </table>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="item">
    <tr class="product">
     <td>
         <xsl:element name="img">
             <xsl:attribute name="width">200px</xsl:attribute>
             <xsl:attribute name="height">200px</xsl:attribute>
             <xsl:attribute name="class">rounded float-left</xsl:attribute>
             <xsl:attribute name="src">
                 <xsl:value-of select="image"/>
             </xsl:attribute>
         </xsl:element>
     </td>
     <td align="center" class="align-middle">
        <p class="lead">
            <xsl:value-of select="description"/>
        </p>
     </td>
     <td align="center" class="align-middle">
         <p class="lead">
            <xsl:value-of select="price"/> грн.
         </p>
     </td>
    </tr>
  </xsl:template>
</xsl:stylesheet>