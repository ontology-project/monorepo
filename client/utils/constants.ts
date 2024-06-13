// export const BASE_URL = 'http://localhost:8000/api'
export const BASE_URL = 'https://ontologyresearch.cs.ui.ac.id/api'

export const EXCEL_TEMPLATE_URL =
  'https://docs.google.com/spreadsheets/d/1lDcFnYP5eo40tF3rCqgclSB2JsucMRsG/edit?usp=sharing&ouid=111756438301550504739&rtpof=true&sd=true'

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
  'TeachingLearningActivity',
]

export const RELATIONSHIPS = [
  'allignWith',
  'belongsToCurr',
  'belongsToSP',
  'coveredInCourse',
  'coversContent',
  'hasCLO',
  'hasCondition',
  'hasCourse',
  'hasCriteria',
  'hasCurriculum',
  'hasDomain',
  'hasPart',
  'hasPEO',
  'hasPerformance',
  'includedInCourse',
  'includedInCurr',
  'partOf',
  'ploHasCourse',
  'satisfies',
]

export const QUERIES = [
  { text: 'PLO', endpoint: '/api/get-plo' },
  { text: 'PLO and the SNDikti components', endpoint: '/api/get-sndikti' },
  { text: 'PLO and the KKNI components', endpoint: '/api/get-kkni' },
  {
    text: 'PLO and Cognitive, Affective, Psychomotoric Domains',
    endpoint: '/api/get-knowledge-cat',
  },
  { text: 'PEO to PLO Mapping', endpoint: '/api/get-peo-map' },
  { text: 'Curriculum Structure', endpoint: '/api/get-curriculum-structure' },
  { text: 'PLO to Course Mapping', endpoint: '/api/get-course-plo-map' },
  { text: 'CLO to Course Mapping', endpoint: '/api/get-course-plo-clo-map' },
]

export const TERMS = [
  { key: 'PLO', value: 'Program Learning Outcomes' },
  { key: 'PEO', value: 'Program Educational Objectives' },
  { key: 'CLO', value: 'Course Learning Outcomes' },
]

export const TOAST_DURATION = 1500
