# Nuture AI

Nuture AI is an AI maternal health adviser, that's designed to educate and help expecting mothers make better and informed decisions. It utilizes generative AI to give personalized answers, making the experience more engaging for users.

Nuture AI is intended to ease access to great and reliable maternal health information.

## Datasets (PDF Files)

All files are available online for free download

1. International Maternal & Child Health Care (Global Women’s Medicine) [donwload](https://www.glowm.com/pdf/International%20Maternal%20and%20Child%20Healthcare%20Textbook.%20A%20practical%20manual%20for%20hospitals%20worldwide%20MCAI%20ALSG.pdf) | [source](https://www.glowm.com/resource-type/resource/textbook/title/international-maternal-and-child-healthcare----a-practical-manual-for-hospitals-worldwide/resource-doc/1968)
2. The Pregnancy Book (St George’s University Hospitals NHS Foundation Trust) [download](https://www.stgeorges.nhs.uk/wp-content/uploads/2013/11/Pregnancy_Book_comp.pdf) | [source](https://www.stgeorges.nhs.uk/)
3. Because Tomorrow Needs Her: The Fight For Women’s Health (Doctors Without Borders) [download](http://womenshealth.msf.org/wp-content/uploads/2015/03/Womens-Health-Book.pdf) | [source](https://www.doctorswithoutborders.org/who-we-are/books-about-msf/because-tomorrow-needs-her)
4. Improving maternal and newborn health and survival and reducing stillbirth - Progress report 2023 (WHO) [download](https://iris.who.int/bitstream/handle/10665/367617/9789240073678-eng.pdf?sequence=1) | [source](https://www.who.int/publications/i/item/9789240073678)

## Tools used

1. **Google gemini (gemini-1.5-flash-001 and models/embedding-001 models)**
2. **LlamaIndex**
3. **Firebase**
4. **Flutter**
5. **FastAPI**

---

### Setup project & Install dependencies

    python -m venv venv
    pip install -r requirements.txt

### Create a /data directory

Create a directory named "data" at the root of your project. Place the documents (you want to use as your knowledge base) into the "data" directory.

---

### Create a .env file

You need to following the following guide to setup service account and add a key to it. This is required for working with google cloud services. [Service account](https://cloud.google.com/iam/docs/keys-create-delete#creating).

_Note: keep the downloaded key safe._

Make a copy of the `.env.example`file and update the value of `GOOGLE_APPLICATION_CREDENTIALS` to the path of your service account key. E.g. `GOOGLE_APPLICATION_CREDENTIALS=path/to/my/key.json`

---

### Run project

```
 python ingest.py
 fastapi dev main.py
```
