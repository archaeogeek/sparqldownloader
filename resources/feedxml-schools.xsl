<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:template match="/">
    <xsl:apply-templates select="/*[name()='sparql']/*[name()='results']">
    </xsl:apply-templates>
  </xsl:template>
  <xsl:template match="//*[name()='results']">
    <schools>
      <xsl:for-each select="./*[name()='result']">
        <school>
          <xsl:for-each select="./*[name()='binding']">
            <xsl:element name="{@name}">
              <xsl:value-of select="*[name()='literal']/text()" />
            </xsl:element>
          </xsl:for-each>
        </school>
      </xsl:for-each>
    </schools>
  </xsl:template>
</xsl:stylesheet>
