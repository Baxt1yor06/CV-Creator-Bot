from jinja2 import Template

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Ahmdd Saah - Resume</title>
  <!-- <link rel="stylesheet" href="style.css" /> -->
  <style>
    * {
      box-sizing: border-box;
      font-family: "Helvetica Neue", Arial, sans-serif;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    body {
      margin: 0;
      padding: 0;
      background: white;
    }

    /* =========================
       PAGE SIZE FOR PDF
    ========================= */
    @page {
      size: A4;
      margin: 20mm;
    }

    /* =========================
       RESUME CONTAINER
    ========================= */
    .resume {
      width: 100%;
      margin: 0;
      padding: 0;
      background: #ffffff;
    }

    /* =========================
       HEADER
    ========================= */
    .header {
      border-bottom: 2px solid #1f3a5f;
      padding-bottom: 10px;
      margin-bottom: 20px;
    }

    .header h1 {
      margin: 0;
      font-size: 28px;
      letter-spacing: 1px;
      color: #1f3a5f;
    }

    .header .title {
      margin-top: 6px;
      font-size: 12px;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: #333;
    }

    /* =========================
       LAYOUT
    ========================= */
    .content {
      display: flex;
      gap: 30px;
    }

    /* Left Column */
    .left {
      width: 32%;
    }

    /* Right Column */
    .right {
      width: 68%;
    }

    /* =========================
       SECTION HEADERS
    ========================= */
    h3 {
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 1px;
      border-bottom: 1px solid #1f3a5f;
      padding-bottom: 4px;
      margin-top: 22px;
      margin-bottom: 10px;
      color: #1f3a5f;
    }

    /* =========================
       TEXT
    ========================= */
    p {
      font-size: 11.5px;
      line-height: 1.6;
      margin: 0 0 8px 0;
      color: #222;
    }

    ul {
      list-style: none;
      padding: 0;
      margin: 0;
    }

    li {
      font-size: 11.5px;
      margin-bottom: 6px;
    }

    /* =========================
       JOB SECTIONS
    ========================= */
    .job {
      margin-bottom: 14px;
      page-break-inside: avoid;
    }

    .job-header {
      display: flex;
      justify-content: space-between;
      font-size: 11.5px;
      font-weight: bold;
    }

    .job-title {
      font-style: italic;
      font-size: 11.5px;
      margin: 4px 0 6px;
    }

    /* =========================
       PRINT-SPECIFIC RULES
    ========================= */
    @media print {
      body {
        background: white;
      }

      .resume {
        box-shadow: none;
      }

      .content {
        gap: 25px;
      }

      section {
        page-break-inside: avoid;
      }

      h3 {
        page-break-after: avoid;
      }
    }


  </style>
</head>
<body>

<div class="resume">
  <!-- Header -->
  <header class="header">
    <h1>{{ full_name | upper }}</h1>
    <p class="title">{{ proffesion }}</p>
  </header>

  <div class="content">
    <!-- Left Column -->
    <aside class="left">
      <section>
        <h3>BOG‘LANISH</h3>
        <ul class="contact">
          <li>{{ phone }}</li>
          <li>{{ email }}</li>
          <li>{{ location }}</li>
          {% if links %}
            <li>{{ links }}</li>
          {% endif %}
        </ul>
      </section>

      <section>
        <h3>KO‘NIKMALAR</h3>
        <ul>
          {% for skill in skills %}
            <li>{{ skill }}</li>
          {% endfor %}
        </ul>
      </section>

      {% if languages %}
      <section>
        <h3>TILLAR</h3>
        <ul>
          {% for lang in languages %}
            <li>{{ lang }}</li>
          {% endfor %}
        </ul>
      </section>
      {% endif %}
    </aside>

    <!-- Right Column -->
    <main class="right">
      {% if about %}
      <section>
        <h3>QISQACHA MA’LUMOT</h3>
        <p>{{ about }}</p>
      </section>
      {% endif %}

      {% if work %}
      <section>
        <h3>ISH TAJRIBASI</h3>
        {% for w in work %}
        <div class="job">
          <div class="job-header">
            <strong>{{ w.company }}</strong>
            <span>{{ w.years }}</span>
          </div>
          <p class="job-title">{{ w.field }}</p>
          <p>{{ w.description }}</p>
        </div>
        {% endfor %}
      </section>
      {% endif %}

      {% if education %}
      <section>
        <h3>TA’LIM</h3>
        {% for edu in education %}
        <div class="job">
          <div class="job-header">
            <strong>{{ edu.place }}</strong>
            <span>{{ edu.years }}</span>
          </div>
          <p>{{ edu.field }}</p>
        </div>
        {% endfor %}
      </section>
      {% endif %}
      
    </main>
  </div>
</div>

</body>
</html>

"""

def render_cv(data: dict) -> str:
  template = Template(HTML_TEMPLATE)
  return template.render(**data)
