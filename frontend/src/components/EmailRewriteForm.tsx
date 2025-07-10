import axios from "axios";
import { useFormik } from "formik";
import React, { useEffect, useState } from "react";

interface ILanguage {
  id: number;
  code: string;
  name: string;
}

interface IContext {
  id: number;
  name: string;
}

interface IStyle {
  id: number;
  name: string;
}

interface IEmailItemResponse {
  subject: string;
  body: string;
}

export const EmailRewriteForm: React.FC = () => {
  const [languages, setLanguages] = useState<ILanguage[]>([]);
  const [contexts, setContexts] = useState<IContext[]>([]);
  const [styles, setStyles] = useState<IStyle[]>([]);
  const [emails, setEmails] = useState<IEmailItemResponse[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const loadLanguages = () => {
    axios
      .get<{ languages: ILanguage[] }>("http://127.0.0.1:8000/api/languages/")
      .then((response) => {
        setLanguages(response.data.languages);
      })
      .catch((error) => {
        console.log("Error loading languages: ", error);
      });
  };

  const loadContexts = () => {
    axios
      .get<{ contexts: IContext[] }>("http://127.0.0.1:8000/api/contexts/")
      .then((response) => {
        setContexts(response.data.contexts);
      })
      .catch((error) => {
        console.log("Error loading contexts: ", error);
      });
  };

  const loadStyles = () => {
    axios
      .get<{ styles: IStyle[] }>("http://127.0.0.1:8000/api/styles/")
      .then((response) => {
        setStyles(response.data.styles);
      })
      .catch((error) => {
        console.log("Error loading styles: ", error);
      });
  };

  useEffect(() => {
    loadLanguages();
    loadContexts();
    loadStyles();
  }, []);

  const formHandler = useFormik({
    initialValues: {
      emailContent: "",
      styleId: "",
      contextId: "",
      languageId: "",
    },

    onSubmit: async (values) => {
      const payload = {
        email: values.emailContent,
        style_id: parseInt(values.styleId),
        context_id: parseInt(values.contextId),
        language_id: parseInt(values.languageId),
      };
      console.log('payload : ', payload)
      setLoading(true);

      try {
        const response = await axios.post<{ emails: IEmailItemResponse[] }>(
          "http://127.0.0.1:8000/api/rewriter/",
          payload
        );
        setEmails(response.data.emails);
        setLoading(false)
      } catch (error) {
        console.log(error);
      }finally{
        setLoading(false)
      }
    },
  });

  return (
    <>
      <form onSubmit={formHandler.handleSubmit}>
        <div>
          <label htmlFor="email">Email for translation : </label>
          <textarea {...formHandler.getFieldProps("emailContent")}></textarea>
        </div>
        <div>
          <label htmlFor="style">Style</label>
          <select {...formHandler.getFieldProps("styleId")}>
            <option value="" disabled selected>
              Select a style
            </option>
            {styles.map((style) => (
              <option key={style.id} value={style.id}>
                {style.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="context">Context</label>
          <select {...formHandler.getFieldProps("contextId")}>
            <option value="" disabled selected>
              Select a context
            </option>
            {contexts.map((context) => (
              <option key={context.id} value={context.id}>
                {context.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="language">Language</label>
          <select {...formHandler.getFieldProps("languageId")} >
            <option value="" disabled selected>
              Select a language
            </option>
            {languages.map((language) => (
              <option key={language.code} value={language.id}>
                {language.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <button type="submit">Generate</button>
        </div>
      </form>

      <div>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <div>
            {emails.map((email, index) => (
              <div key={index}>
                <h3>{email.subject}</h3>
                <p>{email.body}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
};
