import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const API_BASE = import.meta.env.VITE_API_BASE || '';  // Empty default uses same-origin API for Railway/Docker deployments

const translations = {
  en: {
    appTitle: 'Shakti Scheme Application',
    appSubtitle: 'Citizen data collection for transport schemes and passes',
    newApplication: 'New Application',
    applications: 'Applications',
    schemes: 'Schemes & Passes',
    statistics: 'Statistics',
    settings: 'Settings',
    users: 'User Management',
    language: 'Language',
    submit: 'Submit Application',
    reset: 'Reset',
    saveSuccess: 'Application submitted successfully',
    citizen: 'Citizen Details',
    eligibility: 'Eligibility & Proof',
    schemeSelection: 'Scheme & Validity',
    aadhaar: 'Aadhaar & 5 Guarantee',
    address: 'Address',
    consent: 'Consent',
    nameEn: 'Full Name',
    nameKn: 'Name in Kannada',
    age: 'Age',
    dob: 'Date of Birth',
    gender: 'Gender',
    category: 'Category',
    mobile: 'Mobile Number',
    email: 'Email',
    scheme: 'Scheme',
    passType: 'Pass Type',
    validity: 'Validity Requested',
    validityStart: 'Validity Start',
    validityEnd: 'Validity End',
    proofType: 'Proof Type',
    proofReference: 'Proof Reference No.',
    proofUpload: 'Proof Upload',
    proofFrontUpload: 'Proof Front Page',
    proofBackUpload: 'Proof Back Page',
    proofJpgOnly: 'Upload JPG files only. Use clear front and back images of the eligibility proof document.',
    nameAutoKannada: 'Kannada name is auto-suggested from the English name and can be edited manually.',
    photo: 'Citizen Photograph',
    uploadPhoto: 'Upload Photograph',
    openCamera: 'Open Camera',
    capturePhoto: 'Capture Photo',
    closeCamera: 'Close Camera',
    photoHint: 'Upload an image or capture from camera. On mobile, the file picker can directly open the camera.',
    aadhaarNo: 'Aadhaar Number',
    aadhaarName: 'Name as per Aadhaar',
    aadhaarDob: 'DOB as per Aadhaar',
    aadhaarGender: 'Gender as per Aadhaar',
    guaranteeNo: '5 Guarantee Scheme Application No.',
    address1: 'Address Line 1',
    address2: 'Address Line 2',
    district: 'District',
    taluk: 'Taluk',
    city: 'City / Town',
    pincode: 'PIN Code',
    institution: 'School / College / Institution',
    employer: 'Employer / Company',
    route: 'Preferred Route / Corridor',
    service: 'Preferred Service',
    remarks: 'Remarks',
    dataConsent: 'I consent to use my data for application processing.',
    aadhaarConsent: 'I consent to Aadhaar / identity verification as applicable.',
    termsConsent: 'I confirm that the information provided is correct.',
    requiredNote: 'Required fields are marked with *',
    applicationNo: 'Application No.',
    status: 'Status',
    created: 'Created',
    search: 'Search applications',
    noRecords: 'No records yet',
    totalApplications: 'Total Applications',
    totalUsers: 'Total Users',
    byScheme: 'Applications by Scheme',
    byCategory: 'Applications by Category',
    productionNote: 'Production note: store Aadhaar and proof documents only with encryption, access logs, consent, and statutory compliance controls.',
    version: 'Version',
    build: 'Build',
    releaseDate: 'Release Date',
    releaseHistory: 'Release History',
    database: 'Database',
    footerProduct: 'Government Scheme Application Prototype',
    aiAssist: 'AI-assisted recommendation',
    aiAssistText: 'Only eligible pass types are shown for the selected scheme. The recommended pass and validity are auto-selected.',
    ruleBased: 'Local explainable AI rules',
    details: 'Details',
    allowedPassTypes: 'Allowed Pass Types',
    eligibleCategories: 'Eligible Categories',
    serviceScope: 'Service Scope',
    validityRule: 'Validity Rule',
    createUser: 'Create User',
    userList: 'User List',
    username: 'Username',
    fullName: 'Full Name',
    role: 'Role',
    password: 'Password',
    active: 'Active',
    inactive: 'Inactive',
    deactivate: 'Deactivate',
    activate: 'Activate',
    create: 'Create',
    userCreated: 'User created successfully',
    defaultAdminNote: 'Default demo admin: Admin / admin123. Change this before production use.',
    info: 'Information',
    requiredFieldsInfo: 'Fields marked with * are mandatory. Use the information icon beside fields and sections for guidance.',
    autoEndInfo: 'End date is calculated automatically from the selected start date and requested validity period.',
    ageInfo: 'Age is calculated from Date of Birth and kept read-only to avoid manual errors.',
    settingsInfo: 'This application uses Python FastAPI, React NodeJS, and SQLite for prototype/demo purposes.',
    featureInfo: 'Configured application capabilities are shown as compact chips. Detailed notes are available in release history.',
  },
  kn: {
    appTitle: 'ಶಕ್ತಿ ಯೋಜನೆ ಅರ್ಜಿ',
    appSubtitle: 'ಸಾರಿಗೆ ಯೋಜನೆಗಳು ಮತ್ತು ಪಾಸ್‌ಗಳಿಗೆ ನಾಗರಿಕರ ಮಾಹಿತಿ ಸಂಗ್ರಹ',
    newApplication: 'ಹೊಸ ಅರ್ಜಿ',
    applications: 'ಅರ್ಜಿಗಳು',
    schemes: 'ಯೋಜನೆಗಳು ಮತ್ತು ಪಾಸ್‌ಗಳು',
    statistics: 'ಅಂಕಿಅಂಶಗಳು',
    settings: 'ಸೆಟ್ಟಿಂಗ್‌ಗಳು',
    users: 'ಬಳಕೆದಾರ ನಿರ್ವಹಣೆ',
    language: 'ಭಾಷೆ',
    submit: 'ಅರ್ಜಿ ಸಲ್ಲಿಸಿ',
    reset: 'ಮರುಹೊಂದಿಸಿ',
    saveSuccess: 'ಅರ್ಜಿ ಯಶಸ್ವಿಯಾಗಿ ಸಲ್ಲಿಸಲಾಗಿದೆ',
    citizen: 'ನಾಗರಿಕರ ವಿವರಗಳು',
    eligibility: 'ಅರ್ಹತೆ ಮತ್ತು ದಾಖಲೆ',
    schemeSelection: 'ಯೋಜನೆ ಮತ್ತು ಮಾನ್ಯತೆ',
    aadhaar: 'ಆಧಾರ್ ಮತ್ತು 5 ಗ್ಯಾರಂಟಿ',
    address: 'ವಿಳಾಸ',
    consent: 'ಸಮ್ಮತಿ',
    nameEn: 'ಪೂರ್ಣ ಹೆಸರು',
    nameKn: 'ಕನ್ನಡದಲ್ಲಿ ಹೆಸರು',
    age: 'ವಯಸ್ಸು',
    dob: 'ಜನ್ಮ ದಿನಾಂಕ',
    gender: 'ಲಿಂಗ',
    category: 'ವರ್ಗ',
    mobile: 'ಮೊಬೈಲ್ ಸಂಖ್ಯೆ',
    email: 'ಇಮೇಲ್',
    scheme: 'ಯೋಜನೆ',
    passType: 'ಪಾಸ್ ಪ್ರಕಾರ',
    validity: 'ಕೋರಿದ ಮಾನ್ಯತೆ',
    validityStart: 'ಮಾನ್ಯತೆ ಪ್ರಾರಂಭ',
    validityEnd: 'ಮಾನ್ಯತೆ ಅಂತ್ಯ',
    proofType: 'ದಾಖಲೆ ಪ್ರಕಾರ',
    proofReference: 'ದಾಖಲೆ ಉಲ್ಲೇಖ ಸಂಖ್ಯೆ',
    proofUpload: 'ದಾಖಲೆ ಅಪ್ಲೋಡ್',
    proofFrontUpload: 'ದಾಖಲೆ ಮುಂಭಾಗ',
    proofBackUpload: 'ದಾಖಲೆ ಹಿಂಭಾಗ',
    proofJpgOnly: 'JPG ಫೈಲ್‌ಗಳನ್ನು ಮಾತ್ರ ಅಪ್ಲೋಡ್ ಮಾಡಿ. ಅರ್ಹತೆ ದಾಖಲೆಯ ಸ್ಪಷ್ಟ ಮುಂಭಾಗ ಮತ್ತು ಹಿಂಭಾಗದ ಚಿತ್ರಗಳನ್ನು ಬಳಸಿ.',
    nameAutoKannada: 'ಇಂಗ್ಲಿಷ್ ಹೆಸರಿನಿಂದ ಕನ್ನಡ ಹೆಸರನ್ನು ಸ್ವಯಂ ಸೂಚಿಸಲಾಗುತ್ತದೆ ಮತ್ತು ಕೈಯಾರೆ ಬದಲಾಯಿಸಬಹುದು.',
    photo: 'ನಾಗರಿಕರ ಫೋಟೋ',
    uploadPhoto: 'ಫೋಟೋ ಅಪ್ಲೋಡ್',
    openCamera: 'ಕ್ಯಾಮೆರಾ ತೆರೆಯಿರಿ',
    capturePhoto: 'ಫೋಟೋ ತೆಗೆದುಕೊಳ್ಳಿ',
    closeCamera: 'ಕ್ಯಾಮೆರಾ ಮುಚ್ಚಿ',
    photoHint: 'ಚಿತ್ರವನ್ನು ಅಪ್ಲೋಡ್ ಮಾಡಿ ಅಥವಾ ಕ್ಯಾಮೆರಾದಿಂದ ಫೋಟೋ ತೆಗೆದುಕೊಳ್ಳಿ. ಮೊಬೈಲ್‌ನಲ್ಲಿ ಫೈಲ್ ಪಿಕರ್ ನೇರವಾಗಿ ಕ್ಯಾಮೆರಾ ತೆರೆಯಬಹುದು.',
    aadhaarNo: 'ಆಧಾರ್ ಸಂಖ್ಯೆ',
    aadhaarName: 'ಆಧಾರ್‌ನಲ್ಲಿರುವ ಹೆಸರು',
    aadhaarDob: 'ಆಧಾರ್‌ನಲ್ಲಿರುವ ಜನ್ಮ ದಿನಾಂಕ',
    aadhaarGender: 'ಆಧಾರ್‌ನಲ್ಲಿರುವ ಲಿಂಗ',
    guaranteeNo: '5 ಗ್ಯಾರಂಟಿ ಯೋಜನೆ ಅರ್ಜಿ ಸಂಖ್ಯೆ',
    address1: 'ವಿಳಾಸ ಸಾಲು 1',
    address2: 'ವಿಳಾಸ ಸಾಲು 2',
    district: 'ಜಿಲ್ಲೆ',
    taluk: 'ತಾಲ್ಲೂಕು',
    city: 'ನಗರ / ಪಟ್ಟಣ',
    pincode: 'ಪಿನ್ ಕೋಡ್',
    institution: 'ಶಾಲೆ / ಕಾಲೇಜು / ಸಂಸ್ಥೆ',
    employer: 'ಉದ್ಯೋಗದಾತ / ಕಂಪನಿ',
    route: 'ಆದ್ಯತೆಯ ಮಾರ್ಗ / ಕಾರಿಡಾರ್',
    service: 'ಆದ್ಯತೆಯ ಸೇವೆ',
    remarks: 'ಟಿಪ್ಪಣಿ',
    dataConsent: 'ಅರ್ಜಿ ಪ್ರಕ್ರಿಯೆಗೆ ನನ್ನ ಮಾಹಿತಿಯನ್ನು ಬಳಸಲು ನಾನು ಸಮ್ಮತಿಸುತ್ತೇನೆ.',
    aadhaarConsent: 'ಅನ್ವಯವಾಗುವಂತೆ ಆಧಾರ್ / ಗುರುತಿನ ಪರಿಶೀಲನೆಗೆ ನಾನು ಸಮ್ಮತಿಸುತ್ತೇನೆ.',
    termsConsent: 'ನಾನು ನೀಡಿದ ಮಾಹಿತಿ ಸರಿಯಾಗಿದೆ ಎಂದು ದೃಢಪಡಿಸುತ್ತೇನೆ.',
    requiredNote: 'ಅವಶ್ಯಕ ಕ್ಷೇತ್ರಗಳನ್ನು * ಗುರುತಿಸಲಾಗಿದೆ',
    applicationNo: 'ಅರ್ಜಿ ಸಂಖ್ಯೆ',
    status: 'ಸ್ಥಿತಿ',
    created: 'ರಚಿಸಿದ ದಿನಾಂಕ',
    search: 'ಅರ್ಜಿಗಳನ್ನು ಹುಡುಕಿ',
    noRecords: 'ಇನ್ನೂ ದಾಖಲೆಗಳಿಲ್ಲ',
    totalApplications: 'ಒಟ್ಟು ಅರ್ಜಿಗಳು',
    totalUsers: 'ಒಟ್ಟು ಬಳಕೆದಾರರು',
    byScheme: 'ಯೋಜನೆಯ ಪ್ರಕಾರ ಅರ್ಜಿಗಳು',
    byCategory: 'ವರ್ಗದ ಪ್ರಕಾರ ಅರ್ಜಿಗಳು',
    productionNote: 'ಉತ್ಪಾದನಾ ಸೂಚನೆ: ಆಧಾರ್ ಮತ್ತು ದಾಖಲೆಗಳನ್ನು ಎನ್‌ಕ್ರಿಪ್ಷನ್, ಪ್ರವೇಶ ಲಾಗ್, ಸಮ್ಮತಿ ಮತ್ತು ಕಾನೂನು ನಿಯಂತ್ರಣಗಳೊಂದಿಗೆ ಮಾತ್ರ ಸಂಗ್ರಹಿಸಿ.',
    version: 'ಆವೃತ್ತಿ',
    build: 'ಬಿಲ್ಡ್',
    releaseDate: 'ಬಿಡುಗಡೆ ದಿನಾಂಕ',
    releaseHistory: 'ಬಿಡುಗಡೆ ಇತಿಹಾಸ',
    database: 'ಡೇಟಾಬೇಸ್',
    footerProduct: 'ಸರ್ಕಾರಿ ಯೋಜನೆ ಅರ್ಜಿ ಮಾದರಿ',
    aiAssist: 'ಎಐ ಸಹಾಯಿತ ಶಿಫಾರಸು',
    aiAssistText: 'ಆಯ್ಕೆ ಮಾಡಿದ ಯೋಜನೆಗೆ ಸಂಬಂಧಿಸಿದ ಪಾಸ್‌ಗಳನ್ನೇ ತೋರಿಸಲಾಗುತ್ತದೆ. ಶಿಫಾರಸು ಮಾಡಿದ ಪಾಸ್ ಮತ್ತು ಮಾನ್ಯತೆ ಸ್ವಯಂ ಆಯ್ಕೆ ಆಗುತ್ತದೆ.',
    ruleBased: 'ಸ್ಥಳೀಯ ವಿವರಿಸಬಹುದಾದ ಎಐ ನಿಯಮಗಳು',
    details: 'ವಿವರಗಳು',
    allowedPassTypes: 'ಅನುಮತಿಸಿದ ಪಾಸ್ ಪ್ರಕಾರಗಳು',
    eligibleCategories: 'ಅರ್ಹ ವರ್ಗಗಳು',
    serviceScope: 'ಸೇವೆಯ ವ್ಯಾಪ್ತಿ',
    validityRule: 'ಮಾನ್ಯತೆ ನಿಯಮ',
    createUser: 'ಬಳಕೆದಾರ ರಚಿಸಿ',
    userList: 'ಬಳಕೆದಾರರ ಪಟ್ಟಿ',
    username: 'ಬಳಕೆದಾರ ಹೆಸರು',
    fullName: 'ಪೂರ್ಣ ಹೆಸರು',
    role: 'ಪಾತ್ರ',
    password: 'ಪಾಸ್ವರ್ಡ್',
    active: 'ಸಕ್ರಿಯ',
    inactive: 'ನಿಷ್ಕ್ರಿಯ',
    deactivate: 'ನಿಷ್ಕ್ರಿಯಗೊಳಿಸಿ',
    activate: 'ಸಕ್ರಿಯಗೊಳಿಸಿ',
    create: 'ರಚಿಸಿ',
    userCreated: 'ಬಳಕೆದಾರ ಯಶಸ್ವಿಯಾಗಿ ರಚಿಸಲಾಗಿದೆ',
    defaultAdminNote: 'ಡೆಮೊ ಆಡ್ಮಿನ್: Admin / admin123. ಉತ್ಪಾದನೆಗೆ ಮುನ್ನ ಬದಲಿಸಿ.',
    info: 'ಮಾಹಿತಿ',
    requiredFieldsInfo: ' * ಗುರುತಿರುವ ಕ್ಷೇತ್ರಗಳು ಕಡ್ಡಾಯ. ಕ್ಷೇತ್ರಗಳು ಮತ್ತು ವಿಭಾಗಗಳ ಪಕ್ಕದ ಮಾಹಿತಿ ಐಕಾನ್ ಮೂಲಕ ಮಾರ್ಗದರ್ಶನ ನೋಡಿ.',
    autoEndInfo: 'ಆಯ್ಕೆ ಮಾಡಿದ ಪ್ರಾರಂಭ ದಿನಾಂಕ ಮತ್ತು ಕೋರಿದ ಮಾನ್ಯತಾ ಅವಧಿಯಿಂದ ಅಂತ್ಯ ದಿನಾಂಕ ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಲೆಕ್ಕಿಸಲಾಗುತ್ತದೆ.',
    ageInfo: 'ಜನ್ಮ ದಿನಾಂಕದಿಂದ ವಯಸ್ಸನ್ನು ಲೆಕ್ಕಿಸಿ, ಕೈಯಾರೆ ಬದಲಾವಣೆ ತಪ್ಪಿಸಲು ಓದಲು ಮಾತ್ರ ಇಡಲಾಗಿದೆ.',
    settingsInfo: 'ಈ ಅಪ್ಲಿಕೇಶನ್ ಮಾದರಿ/ಡೆಮೊ ಉದ್ದೇಶಕ್ಕೆ Python FastAPI, React NodeJS ಮತ್ತು SQLite ಬಳಸುತ್ತದೆ.',
    featureInfo: 'ಅಪ್ಲಿಕೇಶನ್ ಸಾಮರ್ಥ್ಯಗಳನ್ನು ಸಂಕ್ಷಿಪ್ತ ಚಿಪ್‌ಗಳಾಗಿ ತೋರಿಸಲಾಗಿದೆ. ವಿವರವಾದ ಟಿಪ್ಪಣಿಗಳು ಬಿಡುಗಡೆ ಇತಿಹಾಸದಲ್ಲಿ ಲಭ್ಯ.',
  }
};

const blankForm = {
  scheme_code: 'shakti',
  pass_type_code: 'shakti_smart',
  validity_type: 'Annual',
  validity_start: '',
  validity_end: '',
  name_en: '',
  name_kn: '',
  age: '',
  date_of_birth: '',
  gender: '',
  category_code: 'woman',
  category_other: '',
  mobile: '',
  email: '',
  aadhaar_number: '',
  aadhaar_name: '',
  aadhaar_dob: '',
  aadhaar_gender: '',
  five_guarantee_application_no: '',
  address_line_1: '',
  address_line_2: '',
  district: '',
  taluk: '',
  city: '',
  pincode: '',
  proof_type: '',
  proof_reference_no: '',
  institution_name: '',
  employer_name: '',
  route_preference: '',
  service_preference: '',
  consent_data_use: false,
  consent_aadhaar_verification: false,
  consent_terms: false,
  remarks: ''
};

function calculateAge(dob) {
  if (!dob) return '';
  const birth = new Date(`${dob}T00:00:00`);
  if (Number.isNaN(birth.getTime())) return '';
  const today = new Date();
  let age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) age -= 1;
  return age >= 0 && age <= 130 ? age : '';
}


const KANNADA_INITIALS = {
  a: 'ಎ', b: 'ಬಿ', c: 'ಸಿ', d: 'ಡಿ', e: 'ಇ', f: 'ಎಫ್', g: 'ಜಿ', h: 'ಎಚ್', i: 'ಐ', j: 'ಜೆ', k: 'ಕೆ', l: 'ಎಲ್', m: 'ಎಂ',
  n: 'ಎನ್', o: 'ಓ', p: 'ಪಿ', q: 'ಕ್ಯೂ', r: 'ಆರ್', s: 'ಎಸ್', t: 'ಟಿ', u: 'ಯು', v: 'ವಿ', w: 'ಡಬ್ಲ್ಯೂ', x: 'ಎಕ್ಸ್', y: 'ವೈ', z: 'ಝಡ್'
};

const KANNADA_NAME_OVERRIDES = {
  lakshmi: 'ಲಕ್ಷ್ಮಿ', laxmi: 'ಲಕ್ಷ್ಮಿ', shakti: 'ಶಕ್ತಿ', shakthi: 'ಶಕ್ತಿ', gowri: 'ಗೌರಿ', gauri: 'ಗೌರಿ',
  pooja: 'ಪೂಜಾ', puja: 'ಪೂಜಾ', geetha: 'ಗೀತಾ', gita: 'ಗೀತಾ', seetha: 'ಸೀತಾ', sita: 'ಸೀತಾ',
  savitha: 'ಸವಿತಾ', savita: 'ಸವಿತಾ', kavitha: 'ಕವಿತಾ', kavita: 'ಕವಿತಾ', anitha: 'ಅನಿತಾ', anita: 'ಅನಿತಾ',
  sunitha: 'ಸುನಿತಾ', sunita: 'ಸುನಿತಾ', asha: 'ಆಶಾ', usha: 'ಉಷಾ', uma: 'ಉಮಾ', rani: 'ರಾಣಿ',
  radha: 'ರಾಧಾ', meena: 'ಮೀನಾ', meenakshi: 'ಮೀನಾಕ್ಷಿ', leela: 'ಲೀಲಾ', lila: 'ಲೀಲಾ',
  deepa: 'ದೀಪಾ', deepti: 'ದೀಪ್ತಿ', divya: 'ದಿವ್ಯಾ', priya: 'ಪ್ರಿಯಾ', priyanka: 'ಪ್ರಿಯಾಂಕಾ',
  rashmi: 'ರಶ್ಮಿ', roopa: 'ರೂಪಾ', rupa: 'ರೂಪಾ', rekha: 'ರೇಖಾ', mangala: 'ಮಂಗಳಾ',
  mahalakshmi: 'ಮಹಾಲಕ್ಷ್ಮಿ', parvathi: 'ಪಾರ್ವತಿ', parvati: 'ಪಾರ್ವತಿ', saraswathi: 'ಸರಸ್ವತಿ', saraswati: 'ಸರಸ್ವತಿ',
  srinivasan: 'ಶ್ರೀನಿವಾಸನ್', srinivas: 'ಶ್ರೀನಿವಾಸ್', sridhar: 'ಶ್ರೀಧರ್', satya: 'ಸತ್ಯ', kumar: 'ಕುಮಾರ್', devi: 'ದೇವಿ', bai: 'ಬಾಯಿ'
};

const KANNADA_VOWELS = {
  a: 'ಅ', aa: 'ಆ', i: 'ಇ', ee: 'ಈ', u: 'ಉ', oo: 'ಊ', e: 'ಎ', ae: 'ಏ', ai: 'ಐ', o: 'ಒ', oa: 'ಓ', ou: 'ಔ'
};

const KANNADA_VOWEL_SIGNS = {
  a: '', aa: 'ಾ', i: 'ಿ', ee: 'ೀ', u: 'ು', oo: 'ೂ', e: 'ೆ', ae: 'ೇ', ai: 'ೈ', o: 'ೊ', oa: 'ೋ', ou: 'ೌ'
};

const KANNADA_CONSONANTS = {
  kh: 'ಖ', gh: 'ಘ', ch: 'ಚ', jh: 'ಝ', th: 'ಥ', dh: 'ಧ', ph: 'ಫ', bh: 'ಭ', sh: 'ಶ',
  k: 'ಕ', g: 'ಗ', c: 'ಕ', j: 'ಜ', t: 'ತ', d: 'ದ', n: 'ನ', p: 'ಪ', b: 'ಬ', m: 'ಮ',
  y: 'ಯ', r: 'ರ', l: 'ಲ', v: 'ವ', w: 'ವ', s: 'ಸ', h: 'ಹ', f: 'ಫ', z: 'ಜ'
};

function transliterateTokenToKannada(token) {
  if (!token) return '';
  const lower = token.toLowerCase();
  if (KANNADA_NAME_OVERRIDES[lower]) return KANNADA_NAME_OVERRIDES[lower];
  if (/^[a-z]$/i.test(token)) return KANNADA_INITIALS[lower] || token;
  let out = '';
  let i = 0;
  while (i < lower.length) {
    if (!/[a-z]/.test(lower[i])) { out += token[i] || lower[i]; i += 1; continue; }
    const vowel2 = lower.slice(i, i + 2);
    const vowel1 = lower.slice(i, i + 1);
    if (KANNADA_VOWELS[vowel2]) { out += KANNADA_VOWELS[vowel2]; i += 2; continue; }
    if (KANNADA_VOWELS[vowel1]) { out += KANNADA_VOWELS[vowel1]; i += 1; continue; }
    let consKey = lower.slice(i, i + 2);
    let cons = KANNADA_CONSONANTS[consKey];
    if (cons) i += 2;
    else { consKey = lower.slice(i, i + 1); cons = KANNADA_CONSONANTS[consKey] || token[i]; i += 1; }
    let sign = '';
    const next2 = lower.slice(i, i + 2);
    const next1 = lower.slice(i, i + 1);
    if (KANNADA_VOWEL_SIGNS[next2] !== undefined) { sign = KANNADA_VOWEL_SIGNS[next2]; i += 2; }
    else if (KANNADA_VOWEL_SIGNS[next1] !== undefined) { sign = KANNADA_VOWEL_SIGNS[next1]; i += 1; }
    else if (i < lower.length && /[a-z]/.test(lower[i])) { sign = '್'; }
    out += cons + sign;
  }
  return out;
}

function transliterateNameToKannada(value) {
  return value
    .split(/(\s+|\.|-|')/)
    .map(part => /^[a-zA-Z]+$/.test(part) ? transliterateTokenToKannada(part) : part)
    .join('')
    .replace(/\s+/g, ' ')
    .trim();
}

function isJpgFile(file) {
  if (!file) return true;
  const lower = (file.name || '').toLowerCase();
  return lower.endsWith('.jpg') || lower.endsWith('.jpeg') || file.type === 'image/jpeg';
}

function toDateInput(date) {
  const yyyy = date.getFullYear();
  const mm = String(date.getMonth() + 1).padStart(2, '0');
  const dd = String(date.getDate()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd}`;
}

function addPeriodInclusive(startDate, validityType) {
  if (!startDate || !validityType || validityType === 'Custom') return '';
  const end = new Date(`${startDate}T00:00:00`);
  if (Number.isNaN(end.getTime())) return '';
  const map = {
    'One Day': { days: 1 },
    'Weekly': { days: 7 },
    'Monthly': { months: 1 },
    'Quarterly': { months: 3 },
    'Annual': { years: 1 },
    'Academic Year': { years: 1 },
    '5 Years': { years: 5 },
  };
  const rule = map[validityType];
  if (!rule) return '';
  if (rule.days) end.setDate(end.getDate() + rule.days - 1);
  if (rule.months) { end.setMonth(end.getMonth() + rule.months); end.setDate(end.getDate() - 1); }
  if (rule.years) { end.setFullYear(end.getFullYear() + rule.years); end.setDate(end.getDate() - 1); }
  return toDateInput(end);
}

function App() {
  const [language, setLanguage] = useState('en');
  const t = translations[language];
  const [active, setActive] = useState('new');
  const [master, setMaster] = useState({ schemes: [], pass_types: [], categories: [], pass_rules: {}, pass_validity_rules: {}, user_roles: [], version: '1.0.8', release_info: null });
  const [versionInfo, setVersionInfo] = useState({ version: '1.0.8', build: '20260701.8', release_date: '2026-07-01', database: 'SQLite' });
  const [versionHistory, setVersionHistory] = useState([]);
  const [applications, setApplications] = useState([]);
  const [stats, setStats] = useState(null);
  const [search, setSearch] = useState('');
  const [toast, setToast] = useState('');

  useEffect(() => {
    loadMaster();
    loadVersion();
    loadVersionHistory();
    loadApplications();
    loadStats();
  }, []);

  async function loadMaster() {
    const res = await fetch(`${API_BASE}/api/master-data`);
    setMaster(await res.json());
  }

  async function loadVersion() {
    const res = await fetch(`${API_BASE}/api/version`);
    setVersionInfo(await res.json());
  }

  async function loadVersionHistory() {
    const res = await fetch(`${API_BASE}/api/version-history`);
    const payload = await res.json();
    setVersionHistory(payload.history || []);
  }

  async function loadApplications(query = '') {
    const suffix = query ? `?search=${encodeURIComponent(query)}` : '';
    const res = await fetch(`${API_BASE}/api/applications${suffix}`);
    setApplications(await res.json());
  }

  async function loadStats() {
    const res = await fetch(`${API_BASE}/api/stats`);
    setStats(await res.json());
  }

  function menuItem(id, label) {
    return <button className={active === id ? 'menu-item active' : 'menu-item'} onClick={() => setActive(id)}>{label}</button>;
  }

  const title = active === 'new' ? t.newApplication : active === 'applications' ? t.applications : active === 'schemes' ? t.schemes : active === 'stats' ? t.statistics : active === 'users' ? t.users : t.settings;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-row">
          <div className="brand-mark">ಶ</div>
          <div className="mobile-brand-copy"><h1>{t.appTitle}</h1></div>
        </div>
        <div className="brand-copy">
          <h1>{t.appTitle}</h1>
          <p>{t.appSubtitle}</p>
        </div>
        <nav>
          {menuItem('new', t.newApplication)}
          {menuItem('applications', t.applications)}
          {menuItem('schemes', t.schemes)}
          {menuItem('users', t.users)}
          {menuItem('stats', t.statistics)}
          {menuItem('settings', t.settings)}
        </nav>
        <FooterVersion t={t} versionInfo={versionInfo} compact />
      </aside>

      <main>
        <header className="topbar">
          <div>
            <span className="eyebrow">Karnataka Transport Benefits</span>
            <h2>{title}</h2>
          </div>
          <div className="topbar-actions">
            <div className="version-badge">v{versionInfo.version || '1.0.8'}</div>
            <div className="language-toggle" aria-label={t.language}>
              <button className={language === 'en' ? 'pill active' : 'pill'} onClick={() => setLanguage('en')}>English</button>
              <button className={language === 'kn' ? 'pill active' : 'pill'} onClick={() => setLanguage('kn')}>ಕನ್ನಡ</button>
            </div>
          </div>
        </header>

        {toast && <div className="toast">{toast}</div>}

        {active === 'new' && <ApplicationForm t={t} language={language} master={master} onSaved={() => { setToast(t.saveSuccess); setTimeout(() => setToast(''), 3500); loadApplications(); loadStats(); }} />}
        {active === 'applications' && <Applications t={t} applications={applications} search={search} setSearch={setSearch} onSearch={loadApplications} />}
        {active === 'schemes' && <Schemes t={t} language={language} master={master} />}
        {active === 'users' && <UserManagement t={t} master={master} onChanged={loadStats} />}
        {active === 'stats' && <Stats t={t} stats={stats} />}
        {active === 'settings' && <Settings t={t} language={language} versionInfo={versionInfo} versionHistory={versionHistory} />}
        <FooterVersion t={t} versionInfo={versionInfo} />
      </main>
    </div>
  );
}

function FooterVersion({ t, versionInfo, compact = false }) {
  const version = versionInfo.version || '1.0.8';
  const build = versionInfo.build || '20260701.8';
  const releaseDate = versionInfo.release_date || '2026-07-01';
  const database = versionInfo.database || 'SQLite';
  const status = versionInfo.status || 'Prototype';

  if (compact) {
    return (
      <div className="sidebar-footer">
        <div className="footer-title">{t.footerProduct}</div>
        <div>v{version} · Build {build}</div>
        <div>{t.releaseDate}: {releaseDate}</div>
        <div>{t.database}: {database} · {t.status}: {status}</div>
      </div>
    );
  }

  return (
    <footer className="app-footer" aria-label="Application version details">
      <div>
        <strong>{t.appTitle}</strong>
        <span>{t.footerProduct}</span>
      </div>
      <div className="footer-version-grid">
        <span>{t.version}: <b>v{version}</b></span>
        <span>{t.build}: <b>{build}</b></span>
        <span>{t.releaseDate}: <b>{releaseDate}</b></span>
        <span>{t.database}: <b>{database}</b></span>
        <span>{t.status}: <b>{status}</b></span>
      </div>
    </footer>
  );
}

function HelpTip({ text, label = 'Information' }) {
  const safeText = String(text || '').replace(/undefined|null/g, '').trim();
  if (!safeText) return null;
  return (
    <span className="help-wrap">
      <button type="button" className="info-dot" aria-label={label} title={safeText} onClick={e => { e.preventDefault(); e.stopPropagation(); }} onMouseDown={e => e.stopPropagation()}>i</button>
      <span className="tooltip-box" role="tooltip">{safeText}</span>
    </span>
  );
}

function Field({ label, required, children, hint, infoLabel }) {
  return (
    <label className="field">
      <span className="field-label">
        <span>{label}{required ? <b> *</b> : null}</span>
        <HelpTip text={hint} label={infoLabel || label} />
      </span>
      {children}
    </label>
  );
}

function ApplicationForm({ t, language, master, onSaved }) {
  const [form, setForm] = useState(blankForm);
  const [proofFrontFile, setProofFrontFile] = useState(null);
  const [proofBackFile, setProofBackFile] = useState(null);
  const [nameKnEdited, setNameKnEdited] = useState(false);
  const [photoFile, setPhotoFile] = useState(null);
  const [photoPreview, setPhotoPreview] = useState('');
  const [photoDataUrl, setPhotoDataUrl] = useState('');
  const [cameraOn, setCameraOn] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const nameKey = language === 'kn' ? 'name_kn' : 'name_en';

  const selectedRule = master.pass_rules?.[form.scheme_code] || {};
  const allowedPassTypes = selectedRule.allowed_pass_types || master.pass_types.map(p => p.code);
  const passOptions = master.pass_types.filter(p => allowedPassTypes.includes(p.code));
  const selectedPassRule = master.pass_validity_rules?.[form.pass_type_code] || {};
  const validityOptions = selectedPassRule.options || ['One Day', 'Weekly', 'Monthly', 'Annual', 'Custom'];
  const selectedPass = master.pass_types.find(p => p.code === form.pass_type_code);

  useEffect(() => {
    return () => stopCamera();
  }, []);

  useEffect(() => {
    if (!form.validity_start) return;
    const nextEnd = addPeriodInclusive(form.validity_start, form.validity_type);
    if (nextEnd && nextEnd !== form.validity_end) {
      setForm(prev => ({ ...prev, validity_end: nextEnd }));
    }
  }, [form.validity_start, form.validity_type, form.pass_type_code]);

  function update(key, value) {
    setForm(prev => ({ ...prev, [key]: value }));
  }

  function handleEnglishNameChange(value) {
    const suggestedKannadaName = transliterateNameToKannada(value);
    setForm(prev => ({
      ...prev,
      name_en: value,
      name_kn: nameKnEdited ? prev.name_kn : suggestedKannadaName,
    }));
  }

  function handleKannadaNameChange(value) {
    setNameKnEdited(Boolean(value.trim()));
    update('name_kn', value);
  }

  function handleProofFile(kind, event) {
    const file = event.target.files?.[0] || null;
    if (file && !isJpgFile(file)) {
      event.target.value = '';
      setError(t.proofJpgOnly || 'Upload JPG files only.');
      if (kind === 'front') setProofFrontFile(null);
      if (kind === 'back') setProofBackFile(null);
      return;
    }
    setError('');
    if (kind === 'front') setProofFrontFile(file);
    if (kind === 'back') setProofBackFile(file);
  }

  function updateWithAutoEnd(next) {
    const validityEnd = addPeriodInclusive(next.validity_start, next.validity_type);
    return { ...next, validity_end: validityEnd || next.validity_end || '' };
  }

  function handleSchemeChange(value) {
    const rule = master.pass_rules?.[value] || {};
    const defaultPass = rule.default_pass_type || rule.allowed_pass_types?.[0] || master.pass_types[0]?.code || '';
    const passRule = master.pass_validity_rules?.[defaultPass] || {};
    const defaultValidity = rule.default_validity || passRule.default || passRule.options?.[0] || 'Monthly';
    setForm(prev => {
      const eligible = rule.eligible_categories || [];
      const nextCategory = eligible.length && !eligible.includes(prev.category_code) ? eligible[0] : prev.category_code;
      return updateWithAutoEnd({ ...prev, scheme_code: value, pass_type_code: defaultPass, validity_type: defaultValidity, category_code: nextCategory });
    });
  }

  function handlePassChange(value) {
    const passRule = master.pass_validity_rules?.[value] || {};
    const defaultValidity = passRule.default || passRule.options?.[0] || 'Monthly';
    setForm(prev => updateWithAutoEnd({ ...prev, pass_type_code: value, validity_type: defaultValidity }));
  }

  function handleValidityChange(value) {
    setForm(prev => updateWithAutoEnd({ ...prev, validity_type: value }));
  }

  function handleStartChange(value) {
    setForm(prev => updateWithAutoEnd({ ...prev, validity_start: value }));
  }

  function handleDobChange(value) {
    setForm(prev => ({ ...prev, date_of_birth: value, age: calculateAge(value) }));
  }

  function handlePhotoUpload(e) {
    const file = e.target.files?.[0] || null;
    setPhotoFile(file);
    setPhotoDataUrl('');
    setPhotoPreview(file ? URL.createObjectURL(file) : '');
  }

  async function startCamera() {
    setError('');
    if (!navigator.mediaDevices?.getUserMedia) {
      setError('Camera is not available in this browser. Use photograph upload instead.');
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' }, audio: false });
      streamRef.current = stream;
      setCameraOn(true);
      setTimeout(() => {
        if (videoRef.current) videoRef.current.srcObject = stream;
      }, 0);
    } catch (err) {
      setError('Camera permission was not granted or the camera is not available.');
    }
  }

  function stopCamera() {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    setCameraOn(false);
  }

  function capturePhoto() {
    const video = videoRef.current;
    if (!video) return;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
    setPhotoDataUrl(dataUrl);
    setPhotoPreview(dataUrl);
    setPhotoFile(null);
    stopCamera();
  }

  async function submit(e) {
    e.preventDefault();
    setError('');
    setSaving(true);
    try {
      const fd = new FormData();
      const payload = { ...form };
      if (photoDataUrl && !photoFile) payload.citizen_photo_data_url = photoDataUrl;
      fd.append('data_json', JSON.stringify(payload));
      if (proofFrontFile) fd.append('proof_front_file', proofFrontFile);
      if (proofBackFile) fd.append('proof_back_file', proofBackFile);
      if (photoFile) fd.append('citizen_photo_file', photoFile);
      const res = await fetch(`${API_BASE}/api/applications`, { method: 'POST', body: fd });
      if (!res.ok) {
        const payload = await res.json();
        throw new Error(typeof payload.detail === 'string' ? payload.detail : 'Please fill all required fields.');
      }
      setForm(blankForm);
      setProofFrontFile(null);
      setProofBackFile(null);
      setNameKnEdited(false);
      setPhotoFile(null);
      setPhotoDataUrl('');
      setPhotoPreview('');
      stopCamera();
      onSaved();
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  const genderOptions = ['Female', 'Male', 'Transgender', 'Other'];
  const proofTypes = ['Aadhaar', 'Student ID', 'Disability Certificate', 'Senior Citizen ID', 'Armed Forces ID', 'Employer Certificate', 'Institution Letter', 'Other'];

  return (
    <form className="form-grid" onSubmit={submit}>
      <div className="form-help-row"><HelpTip text={t.requiredFieldsInfo || t.requiredNote} label={t.info} /></div>
      {error && <div className="error-box">{error}</div>}

      <Section title={t.schemeSelection}>
        <div className="ai-panel full-row">
          <div>
            <b>{t.aiAssist}</b>
            <span>{t.ruleBased}</span>
            <HelpTip text={`${t.aiAssistText}${selectedRule.ai_reason ? ' ' + selectedRule.ai_reason : ''}`} label={t.aiAssist} />
          </div>
        </div>
        <Field label={t.scheme} required>
          <select value={form.scheme_code} onChange={e => handleSchemeChange(e.target.value)}>
            {master.schemes.map(s => <option key={s.code} value={s.code}>{s[nameKey]} / {s.name_en}</option>)}
          </select>
        </Field>
        <Field label={t.passType} required hint={selectedPassRule.explain}>
          <select value={form.pass_type_code} onChange={e => handlePassChange(e.target.value)}>
            {passOptions.map(p => <option key={p.code} value={p.code}>{p[nameKey]} / {p.name_en}</option>)}
          </select>
        </Field>
        <Field label={t.validity}>
          <select value={form.validity_type} onChange={e => handleValidityChange(e.target.value)}>
            {validityOptions.map(v => <option key={v}>{v}</option>)}
          </select>
        </Field>
        <Field label={t.validityStart}><input type="date" value={form.validity_start} onChange={e => handleStartChange(e.target.value)} /></Field>
        <Field label={t.validityEnd} hint={t.autoEndInfo}><input type="date" value={form.validity_end} readOnly /></Field>
        <div className="recommendation full-row">
          <b>{t.allowedPassTypes}:</b> {passOptions.map(p => p[nameKey]).join(', ')}
          {selectedPass && <span> · Selected: {selectedPass.name_en}</span>}
        </div>
      </Section>

      <Section title={t.citizen}>
        <Field label={t.nameEn} required hint={t.nameAutoKannada}><input value={form.name_en} onChange={e => handleEnglishNameChange(e.target.value)} placeholder="e.g., Lakshmi R" /></Field>
        <Field label={t.nameKn} hint={t.nameAutoKannada}><input value={form.name_kn} onChange={e => handleKannadaNameChange(e.target.value)} placeholder="ಉದಾ., ಲಕ್ಷ್ಮಿ ಆರ್" /></Field>
        <Field label={t.dob}><input type="date" value={form.date_of_birth} onChange={e => handleDobChange(e.target.value)} /></Field>
        <Field label={t.age} hint={t.ageInfo}><input type="number" min="0" max="130" value={form.age} readOnly /></Field>
        <Field label={t.gender} required>
          <select value={form.gender} onChange={e => update('gender', e.target.value)}>
            <option value="">Select</option>
            {genderOptions.map(v => <option key={v}>{v}</option>)}
          </select>
        </Field>
        <Field label={t.mobile} required><input value={form.mobile} onChange={e => update('mobile', e.target.value)} placeholder="10 digit mobile" inputMode="numeric" /></Field>
        <Field label={t.email}><input type="email" value={form.email} onChange={e => update('email', e.target.value)} /></Field>
        <div className="photo-box full-row">
          <div className="photo-preview">{photoPreview ? <img src={photoPreview} alt="Citizen preview" /> : <span>{t.photo}</span>}</div>
          <div className="photo-actions">
            <Field label={t.uploadPhoto} hint={t.photoHint}><input type="file" accept="image/*" capture="user" onChange={handlePhotoUpload} /></Field>
            <div className="camera-buttons">
              {!cameraOn && <button type="button" className="secondary small" onClick={startCamera}>{t.openCamera}</button>}
              {cameraOn && <button type="button" className="secondary small" onClick={capturePhoto}>{t.capturePhoto}</button>}
              {cameraOn && <button type="button" className="secondary small" onClick={stopCamera}>{t.closeCamera}</button>}
            </div>
            {cameraOn && <video className="camera-view" ref={videoRef} autoPlay playsInline muted />}
          </div>
        </div>
      </Section>

      <Section title={t.eligibility}>
        <Field label={t.category} required>
          <select value={form.category_code} onChange={e => update('category_code', e.target.value)}>
            {master.categories.map(c => <option key={c.code} value={c.code}>{c[nameKey]} / {c.name_en}</option>)}
          </select>
        </Field>
        {form.category_code === 'other' && <Field label="Other Category"><input value={form.category_other} onChange={e => update('category_other', e.target.value)} /></Field>}
        <Field label={t.proofType}>
          <select value={form.proof_type} onChange={e => update('proof_type', e.target.value)}>
            <option value="">Select</option>
            {proofTypes.map(v => <option key={v}>{v}</option>)}
          </select>
        </Field>
        <Field label={t.proofReference}><input value={form.proof_reference_no} onChange={e => update('proof_reference_no', e.target.value)} /></Field>
        <Field label={t.proofFrontUpload || 'Proof Front Page'} hint={t.proofJpgOnly}><input type="file" accept=".jpg,.jpeg,image/jpeg" onChange={e => handleProofFile('front', e)} /></Field>
        <Field label={t.proofBackUpload || 'Proof Back Page'} hint={t.proofJpgOnly}><input type="file" accept=".jpg,.jpeg,image/jpeg" onChange={e => handleProofFile('back', e)} /></Field>
        <Field label={t.institution}><input value={form.institution_name} onChange={e => update('institution_name', e.target.value)} /></Field>
        <Field label={t.employer}><input value={form.employer_name} onChange={e => update('employer_name', e.target.value)} /></Field>
        <Field label={t.route}><input value={form.route_preference} onChange={e => update('route_preference', e.target.value)} /></Field>
        <Field label={t.service}><input value={form.service_preference} onChange={e => update('service_preference', e.target.value)} /></Field>
      </Section>

      <Section title={t.aadhaar}>
        <Field label={t.aadhaarNo}><input value={form.aadhaar_number} onChange={e => update('aadhaar_number', e.target.value)} placeholder="XXXX XXXX XXXX" inputMode="numeric" /></Field>
        <Field label={t.aadhaarName}><input value={form.aadhaar_name} onChange={e => update('aadhaar_name', e.target.value)} /></Field>
        <Field label={t.aadhaarDob}><input type="date" value={form.aadhaar_dob} onChange={e => update('aadhaar_dob', e.target.value)} /></Field>
        <Field label={t.aadhaarGender}><input value={form.aadhaar_gender} onChange={e => update('aadhaar_gender', e.target.value)} /></Field>
        <Field label={t.guaranteeNo}><input value={form.five_guarantee_application_no} onChange={e => update('five_guarantee_application_no', e.target.value)} /></Field>
      </Section>

      <Section title={t.address}>
        <Field label={t.address1}><input value={form.address_line_1} onChange={e => update('address_line_1', e.target.value)} /></Field>
        <Field label={t.address2}><input value={form.address_line_2} onChange={e => update('address_line_2', e.target.value)} /></Field>
        <Field label={t.district}><input value={form.district} onChange={e => update('district', e.target.value)} /></Field>
        <Field label={t.taluk}><input value={form.taluk} onChange={e => update('taluk', e.target.value)} /></Field>
        <Field label={t.city}><input value={form.city} onChange={e => update('city', e.target.value)} /></Field>
        <Field label={t.pincode}><input value={form.pincode} onChange={e => update('pincode', e.target.value)} inputMode="numeric" /></Field>
      </Section>

      <Section title={t.consent} wide>
        <label className="check"><input type="checkbox" checked={form.consent_data_use} onChange={e => update('consent_data_use', e.target.checked)} /> {t.dataConsent}</label>
        <label className="check"><input type="checkbox" checked={form.consent_aadhaar_verification} onChange={e => update('consent_aadhaar_verification', e.target.checked)} /> {t.aadhaarConsent}</label>
        <label className="check"><input type="checkbox" checked={form.consent_terms} onChange={e => update('consent_terms', e.target.checked)} /> {t.termsConsent}</label>
        <Field label={t.remarks}><textarea value={form.remarks} onChange={e => update('remarks', e.target.value)} rows="3" /></Field>
      </Section>

      <div className="actions">
        <button type="button" className="secondary" onClick={() => { setForm(blankForm); setPhotoPreview(''); setPhotoDataUrl(''); setPhotoFile(null); }}>{t.reset}</button>
        <button type="submit" disabled={saving}>{saving ? 'Saving...' : t.submit}</button>
      </div>
    </form>
  );
}

function Section({ title, children, wide }) {
  return <section className={wide ? 'card wide' : 'card'}><h3>{title}</h3><div className="section-grid">{children}</div></section>;
}

function Applications({ t, applications, search, setSearch, onSearch }) {
  return (
    <div className="card wide">
      <div className="table-toolbar">
        <input value={search} onChange={e => setSearch(e.target.value)} placeholder={t.search} />
        <button onClick={() => onSearch(search)}>Search</button>
      </div>
      <div className="table-wrap">
        <table>
          <thead>
            <tr><th>{t.applicationNo}</th><th>{t.created}</th><th>{t.nameEn}</th><th>{t.scheme}</th><th>{t.passType}</th><th>{t.category}</th><th>{t.status}</th></tr>
          </thead>
          <tbody>
            {applications.length === 0 && <tr><td colSpan="7" className="empty">{t.noRecords}</td></tr>}
            {applications.map(app => (
              <tr key={app.id}>
                <td>{app.application_no}</td>
                <td>{app.created_at}</td>
                <td>{app.name_en}</td>
                <td>{app.scheme_name_en}</td>
                <td>{app.pass_name_en}</td>
                <td>{app.category_name_en}</td>
                <td><span className="status-chip">{app.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Schemes({ t, language, master }) {
  const [selected, setSelected] = useState(null);
  const nameKey = language === 'kn' ? 'name_kn' : 'name_en';
  const descriptionKey = language === 'kn' ? 'description_kn' : 'description_en';

  function passName(code) {
    return master.pass_types.find(p => p.code === code)?.[nameKey] || code;
  }
  function categoryName(code) {
    return master.categories.find(c => c.code === code)?.[nameKey] || code;
  }

  function openScheme(s) {
    const rule = master.pass_rules?.[s.code] || {};
    setSelected({ type: 'scheme', item: s, rule });
  }
  function openPass(p) {
    const rule = master.pass_validity_rules?.[p.code] || {};
    setSelected({ type: 'pass', item: p, rule });
  }

  return (
    <div className="catalog">
      <section className="card wide">
        <h3>Scheme Master / ಯೋಜನೆ ಪಟ್ಟಿ</h3>
        <div className="catalog-grid">
          {master.schemes.map(s => (
            <div className="catalog-card clickable" key={s.code} role="button" tabIndex="0" onClick={() => openScheme(s)} onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') openScheme(s); }}>
              <b>{s[nameKey]}</b>
              <span>{s.name_en}</span>
              <div className="catalog-actions"><HelpTip text={s[descriptionKey] || s.description_en} label={t.info} /><em>{t.details} →</em></div>
            </div>
          ))}
        </div>
      </section>
      <section className="card wide">
        <h3>Pass Master / ಪಾಸ್ ಪಟ್ಟಿ</h3>
        <div className="catalog-grid">
          {master.pass_types.map(p => (
            <div className="catalog-card clickable" key={p.code} role="button" tabIndex="0" onClick={() => openPass(p)} onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') openPass(p); }}>
              <b>{p[nameKey]}</b>
              <span>{p.name_en}</span>
              <div className="catalog-actions"><HelpTip text={p[descriptionKey] || p.description_en} label={t.info} /><em>{t.details} →</em></div>
            </div>
          ))}
        </div>
      </section>

      {selected && (
        <div className="modal-backdrop" onClick={() => setSelected(null)}>
          <div className="detail-modal" onClick={e => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setSelected(null)}>×</button>
            <span className="eyebrow">{selected.type === 'scheme' ? t.scheme : t.passType}</span>
            <div className="modal-title-row"><h3>{selected.item[nameKey]}</h3><HelpTip text={selected.item[descriptionKey] || selected.item.description_en} label={t.info} /></div>
            {selected.type === 'scheme' ? (
              <div className="detail-grid">
                <div><b>{t.allowedPassTypes}</b><span>{(selected.rule.allowed_pass_types || []).map(passName).join(', ') || '—'}</span></div>
                <div><b>{t.eligibleCategories}</b><span>{(selected.rule.eligible_categories || []).map(categoryName).join(', ') || '—'}</span></div>
                <div><b>{t.serviceScope}</b><span>{selected.rule.service_scope || '—'}</span></div>
                <div><b>{t.aiAssist}</b><span>{selected.rule.ai_reason || '—'}</span></div>
              </div>
            ) : (
              <div className="detail-grid">
                <div><b>{t.validity}</b><span>{(selected.rule.options || []).join(', ') || '—'}</span></div>
                <div><b>{t.validityRule}</b><span>{selected.rule.explain || '—'}</span></div>
                <div><b>Default</b><span>{selected.rule.default || '—'}</span></div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function UserManagement({ t, master, onChanged }) {
  const [users, setUsers] = useState([]);
  const [search, setSearch] = useState('');
  const [error, setError] = useState('');
  const [toast, setToast] = useState('');
  const [newUser, setNewUser] = useState({ username: '', full_name: '', role: 'Data Entry Operator', mobile: '', email: '', password: '' });

  useEffect(() => { loadUsers(); }, []);

  async function loadUsers(query = '') {
    const suffix = query ? `?search=${encodeURIComponent(query)}` : '';
    const res = await fetch(`${API_BASE}/api/users${suffix}`);
    setUsers(await res.json());
  }

  function updateNew(key, value) {
    setNewUser(prev => ({ ...prev, [key]: value }));
  }

  async function create(e) {
    e.preventDefault();
    setError('');
    try {
      const res = await fetch(`${API_BASE}/api/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newUser),
      });
      if (!res.ok) {
        const payload = await res.json();
        throw new Error(typeof payload.detail === 'string' ? payload.detail : 'Please fill all required fields.');
      }
      setNewUser({ username: '', full_name: '', role: 'Data Entry Operator', mobile: '', email: '', password: '' });
      setToast(t.userCreated);
      setTimeout(() => setToast(''), 3000);
      loadUsers();
      onChanged?.();
    } catch (err) {
      setError(err.message);
    }
  }

  async function toggle(user) {
    const res = await fetch(`${API_BASE}/api/users/${user.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_active: user.is_active ? 0 : 1 }),
    });
    if (res.ok) loadUsers(search);
  }

  const roles = master.user_roles?.length ? master.user_roles : ['Admin', 'Data Entry Operator', 'Approver', 'Viewer'];

  return (
    <div className="settings-stack">
      {toast && <div className="toast">{toast}</div>}
      {error && <div className="error-box">{error}</div>}
      <form className="card wide user-form" onSubmit={create}>
        <h3>{t.createUser}</h3>
        <div className="section-grid">
          <Field label={t.username} required><input value={newUser.username} onChange={e => updateNew('username', e.target.value)} /></Field>
          <Field label={t.fullName} required><input value={newUser.full_name} onChange={e => updateNew('full_name', e.target.value)} /></Field>
          <Field label={t.role} required>
            <select value={newUser.role} onChange={e => updateNew('role', e.target.value)}>{roles.map(role => <option key={role}>{role}</option>)}</select>
          </Field>
          <Field label={t.password} required><input type="password" value={newUser.password} onChange={e => updateNew('password', e.target.value)} /></Field>
          <Field label={t.mobile}><input value={newUser.mobile} onChange={e => updateNew('mobile', e.target.value)} inputMode="numeric" /></Field>
          <Field label={t.email}><input type="email" value={newUser.email} onChange={e => updateNew('email', e.target.value)} /></Field>
        </div>
        <div className="actions"><button type="submit">{t.create}</button></div>
        <div className="form-help-row inline"><HelpTip text={t.defaultAdminNote} label={t.info} /></div>
      </form>

      <div className="card wide">
        <h3>{t.userList}</h3>
        <div className="table-toolbar">
          <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search users" />
          <button onClick={() => loadUsers(search)}>Search</button>
        </div>
        <div className="table-wrap">
          <table>
            <thead><tr><th>{t.username}</th><th>{t.fullName}</th><th>{t.role}</th><th>{t.mobile}</th><th>{t.email}</th><th>{t.status}</th><th>Action</th></tr></thead>
            <tbody>
              {users.length === 0 && <tr><td colSpan="7" className="empty">{t.noRecords}</td></tr>}
              {users.map(user => (
                <tr key={user.id}>
                  <td>{user.username}</td>
                  <td>{user.full_name}</td>
                  <td>{user.role}</td>
                  <td>{user.mobile}</td>
                  <td>{user.email}</td>
                  <td><span className={user.is_active ? 'status-chip' : 'status-chip muted-chip'}>{user.is_active ? t.active : t.inactive}</span></td>
                  <td><button className="table-action" onClick={() => toggle(user)}>{user.is_active ? t.deactivate : t.activate}</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function Stats({ t, stats }) {
  if (!stats) return <div className="card">Loading...</div>;
  return (
    <div className="stats-grid">
      <div className="stat-card"><span>{t.totalApplications}</span><strong>{stats.total}</strong></div>
      <div className="stat-card secondary-stat"><span>{t.totalUsers}</span><strong>{stats.users_total || 0}</strong></div>
      <BarList title={t.byScheme} rows={stats.by_scheme} labelKey="scheme" />
      <BarList title={t.byCategory} rows={stats.by_category} labelKey="category" />
    </div>
  );
}

function BarList({ title, rows, labelKey }) {
  const max = Math.max(1, ...rows.map(r => r.count));
  return <div className="card wide"><h3>{title}</h3>{rows.map(row => <div className="bar-row" key={row[labelKey]}><span>{row[labelKey]}</span><div><i style={{ width: `${(row.count / max) * 100}%` }}></i></div><b>{row.count}</b></div>)}</div>;
}

function Settings({ t, versionInfo, versionHistory }) {
  return (
    <div className="settings-stack">
      <div className="card wide settings-card">
        <div className="section-title-row"><h3>Application Configuration / ಅಪ್ಲಿಕೇಶನ್ ಸಂರಚನೆ</h3><HelpTip text={t.settingsInfo} label={t.info} /></div>
        <div className="version-grid">
          <div><span>{t.version}</span><strong>v{versionInfo.version || '1.0.8'}</strong></div>
          <div><span>{t.build}</span><strong>{versionInfo.build || '20260701.8'}</strong></div>
          <div><span>{t.releaseDate}</span><strong>{versionInfo.release_date || '2026-07-01'}</strong></div>
          <div><span>{t.database}</span><strong>{versionInfo.database || 'SQLite'}</strong></div>
          <div><span>{t.status}</span><strong>{versionInfo.status || 'Prototype'}</strong></div>
        </div>
        <div className="section-title-row compact-title"><strong>Capabilities</strong><HelpTip text={`${t.productionNote} ${t.featureInfo}`} label={t.info} /></div>
        <div className="settings-list">
          <span>AI-assisted scheme/pass selection</span>
          <span>Automatic validity calculation</span>
          <span>DOB-based read-only age</span>
          <span>Citizen photo upload/camera capture</span>
          <span>Clickable scheme/pass tiles</span>
          <span>User management</span>
          <span>Mobile optimized UI</span>
        </div>
      </div>

      <div className="card wide settings-card">
        <h3>{t.releaseHistory}</h3>
        <div className="release-list">
          {versionHistory.map(item => (
            <div className="release-item" key={item.version}>
              <div>
                <b>v{item.version}</b>
                <span>{item.title} · Build {item.build} · {item.release_date}</span>
              </div>
              <ul>{(item.changes || []).map(change => <li key={change}>{change}</li>)}</ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);
