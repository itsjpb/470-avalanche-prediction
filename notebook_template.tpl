{%- extends 'basic.tpl' -%}

{% block header %}
<head>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

      .jp-Notebook {
        background-color: #faf8f8;
        overflow: hidden;
      }

      p {
        font-family: "Inter", sans-serif;
        font-size: 1rem;
      }

      .jp-InputArea-editor {
        border-radius: 8px;
        overflow: auto;
      }
    </style>
</head>
{% endblock header %}