export const BASE_URL = "http://localhost:8000";

export const EXCEL_TEMPLATE_URL = "https://docs.google.com/spreadsheets/d/1kHKhEt1I0E1gFF65KNiVEwYD6WYhkYp-UY0v0PASBGU/edit#gid=786139127";

export const NODE_TYPES = [
    'AssesmentTask',
    'Content',
    'Course',
    'Criteria',
    'Curriculum',
    'KnowledgeCategory',
    'LearningDomain',
    'LearningOutcome',
    'ProgramEducationalObjective',
    'StudyProgram',
    'TeachingLearningActivity'
];

export const RELATIONSHIPS = [
    "allignWith",
    "belongsToCurr",
    "belongsToSP",
    "coveredInCourse",
    "coversContent",
    "hasCLO",
    "hasCondition",
    "hasCourse",
    "hasCriteria",
    "hasCurriculum",
    "hasDomain",
    "hasPart",
    "hasPEO",
    "hasPerformance",
    "includedInCourse",
    "includedInCurr",
    "partOf",
    "ploHasCourse",
    "satisfies"
];

export const QUERIES = [
    { text: "Tampilkan daftar CPL (PLO)", endpoint: "/api/get-plo" },
    { text: "Tampilkan daftar CPL (PLO) dan tampilkan komponen-komponen SN-Dikti-nya", endpoint: "/api/get-sndikti" },
    { text: "Tampilkan daftar CPL (PLO) dan tampilkan komponen-komponen KKNI-nya", endpoint: "/api/get-kkni" },
    { text: "Tampilkan daftar CPL (PLO) dan tampilkan aspek-aspek kognitif, afektif dan psikomotorik", endpoint: "/api/get-knowledge-cat" },
    { text: "Tunjukkan PEO yang tidak dipetakan ke PLO", endpoint: "/api/get-peo-map" },
    { text: "Tampilak struktur kurikulum", endpoint: "/api/get-curriculum-structure" },
];