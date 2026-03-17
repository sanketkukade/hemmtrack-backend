from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import os
import json
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow all origins

# Gmail credentials - Railway environment variables वरून येतील
GMAIL_USER = os.environ.get('GMAIL_USER', 'sanketkukade111@gmail.com')
GMAIL_PASS = os.environ.get('GMAIL_PASS', '')  # App Password

@app.route('/')
def home():
    return jsonify({'status': 'HemmTrack Pro Backend Running!', 'version': '1.0'})

@app.route('/send-alert', methods=['POST'])
def send_alert():
    """HIGH Defect Alert — Email with details"""
    try:
        data = request.json
        to_email = data.get('to_email', GMAIL_USER)
        subject  = data.get('subject', '🚨 HIGH Defect Alert — HemmTrack Pro')
        body     = data.get('body', '')
        
        msg = MIMEMultipart()
        msg['From']    = GMAIL_USER
        msg['To']      = to_email
        msg['Subject'] = subject
        
        # HTML body
        html_body = f"""
        <html><body style="font-family:Arial,sans-serif;">
        <div style="background:#cc0000;color:#fff;padding:14px;border-radius:8px;margin-bottom:16px;">
          <h2 style="margin:0;">🚨 HIGH Defect Alert — HemmTrack Pro</h2>
        </div>
        <pre style="background:#f5f5f5;padding:14px;border-radius:6px;font-size:13px;">{body}</pre>
        <div style="margin-top:16px;color:#666;font-size:12px;">
          — HemmTrack Pro V2 | Sanket | Weld Shop Quality Engineer
        </div>
        </body></html>
        """
        msg.attach(MIMEText(html_body, 'html'))
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(msg)
        
        return jsonify({'success': True, 'message': 'Alert email sent!'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/send-onepager', methods=['POST'])
def send_onepager():
    """One-Pager PPT attached email"""
    try:
        data      = request.json
        to_email  = data.get('to_email', GMAIL_USER)
        model     = data.get('model', 'Nexon')
        failure   = data.get('failure', 'Open Hem')
        occ       = data.get('occ', '03')
        demerit   = data.get('demerit', '200')
        rc        = data.get('rc', 'TBD')
        actions   = data.get('actions', 'TBD')
        ecd       = data.get('ecd', 'TBD')
        raybg     = data.get('raybg', 'R')
        station   = data.get('station', 'ST-100')
        press     = data.get('press', '180')
        ppt_b64   = data.get('ppt_base64', None)  # Optional PPT base64
        
        today = datetime.now().strftime('%d %b %Y')
        
        subject = f'🚨 CRITICAL: One-Pager – {failure} (OCC={occ}) – {model} – Status: {raybg}'
        
        html_body = f"""
        <html><body style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;">
        
        <div style="background:#CC0000;color:#fff;padding:14px;border-radius:8px 8px 0 0;">
          <h2 style="margin:0;">🚨 CRITICAL DEFECT ALERT</h2>
          <p style="margin:4px 0 0;">HEMMING OPEN — REAR DOOR</p>
        </div>
        
        <table style="width:100%;border-collapse:collapse;border:1px solid #ddd;">
          <tr style="background:#1F3864;color:#fff;font-weight:700;text-align:center;">
            <td style="padding:8px;border:1px solid #aaa;">Model</td>
            <td style="padding:8px;border:1px solid #aaa;">Failure</td>
            <td style="padding:8px;border:1px solid #aaa;">OCC</td>
            <td style="padding:8px;border:1px solid #aaa;">Demerit</td>
            <td style="padding:8px;border:1px solid #aaa;">RCA</td>
            <td style="padding:8px;border:1px solid #aaa;">ECD</td>
            <td style="padding:8px;border:1px solid #aaa;">Status</td>
          </tr>
          <tr style="text-align:center;">
            <td style="padding:10px;border:1px solid #ddd;font-weight:700;">{model}</td>
            <td style="padding:10px;border:1px solid #ddd;">{failure}</td>
            <td style="padding:10px;border:1px solid #ddd;background:#CC0000;color:#fff;font-weight:900;font-size:18px;">{occ}</td>
            <td style="padding:10px;border:1px solid #ddd;">{demerit}</td>
            <td style="padding:10px;border:1px solid #ddd;text-align:left;">{rc}</td>
            <td style="padding:10px;border:1px solid #ddd;color:#CC0000;font-weight:700;">{ecd}</td>
            <td style="padding:10px;border:1px solid #ddd;background:#FF0000;color:#fff;font-weight:900;">{raybg}</td>
          </tr>
        </table>
        
        <div style="background:#FFF2CC;border:2px solid #CC0000;padding:12px;margin-top:12px;text-align:center;font-weight:700;color:#CC0000;">
          ⚠ IMMEDIATE ACTION REQUIRED | Station: {station} | Pressure: {press} Bar | Date: {today}
        </div>
        
        <div style="margin-top:16px;padding:12px;background:#f5f5f5;border-radius:6px;">
          <b>Actions Taken/Planned:</b><br>{actions}
        </div>
        
        <div style="margin-top:16px;color:#666;font-size:12px;">
          — HemmTrack Pro V2 | Sanket | Weld Shop Quality Engineer
        </div>
        </body></html>
        """
        
        msg = MIMEMultipart()
        msg['From']    = GMAIL_USER
        msg['To']      = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))
        
        # Attach PPT if provided
        if ppt_b64:
            ppt_data = base64.b64decode(ppt_b64)
            part = MIMEBase('application', 'vnd.openxmlformats-officedocument.presentationml.presentation')
            part.set_payload(ppt_data)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename=Hemming_OnePager_OCC{occ}.pptx')
            msg.attach(part)
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(msg)
        
        return jsonify({'success': True, 'message': 'One-Pager email sent!'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/send-dashboard', methods=['POST'])
def send_dashboard():
    """Dashboard Report Email"""
    try:
        data    = request.json
        to_email = data.get('to_email', GMAIL_USER)
        report  = data.get('report', '')
        date    = data.get('date', datetime.now().strftime('%d %b %Y'))
        
        subject = f'📊 Dashboard Report — HemmTrack Pro — {date}'
        
        html_body = f"""
        <html><body style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;">
        <div style="background:#0066aa;color:#fff;padding:14px;border-radius:8px;margin-bottom:16px;">
          <h2 style="margin:0;">📊 Dashboard Report — HemmTrack Pro</h2>
          <p style="margin:4px 0 0;">📅 {date}</p>
        </div>
        <pre style="background:#f5f5f5;padding:14px;border-radius:6px;font-size:13px;white-space:pre-wrap;">{report}</pre>
        <div style="margin-top:16px;color:#666;font-size:12px;">
          — HemmTrack Pro V2 | Sanket | Weld Shop Quality Engineer
        </div>
        </body></html>
        """
        
        msg = MIMEMultipart()
        msg['From']    = GMAIL_USER
        msg['To']      = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(msg)
        
        return jsonify({'success': True, 'message': 'Dashboard email sent!'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
