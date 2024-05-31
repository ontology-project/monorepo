export const BASE_URL = "http://localhost:8000";

export const EXCEL_TEMPLATE_URL = "https://docs.google.com/spreadsheets/d/148SL5KCIAHdQUPKF2dAc5nJ1OTYFgHQ7vNyzaWeGDzc/edit?usp=sharing";

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
    { text: "Tunjukkan pemetaan PEO ke PLO", endpoint: "/api/get-peo-map" },
    { text: "Tampilkan struktur kurikulum", endpoint: "/api/get-curriculum-structure" },
    { text: "Tampilkan pemetaan PLO ke Mata Kuliah", endpoint: "/api/get-course-plo-map"},
    { text: "Tampilkan pemetaan CLO ke Mata Kuliah", endpoint: "/api/get-course-plo-clo-map"}
];