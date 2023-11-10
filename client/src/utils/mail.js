import nodemailer from "nodemailer";

// create reusable transporter object using the default SMTP transport

const SENDMAIL = async (mailDetails, memberEmail, pass, callback) => {
    const transporter = nodemailer.createTransport({
        service: "gmail",
        host: "smtp.gmail.com",
        port: 587,
        secure: false,
        auth: {
          user: memberEmail,
          pass: pass,
        },
      });
      
    try {
      const info = await transporter.sendMail(mailDetails)
      callback(info);
    } catch (error) {
      console.log(error);
    } 
  };

  export default SENDMAIL;
