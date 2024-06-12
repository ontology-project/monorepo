interface PLOProperty {
  peo?: string
  peoLabel?: string
  plo: string
  ploLabel?: string
  course?: string
}

interface CLOProperty {
  hasCLORel: string
  cloLabel: string
  hasCourse: string
}

interface SNDiktiProperty {
  plo: string
  sndikti_attitude?: string
  sndikti_genericskill?: string
  sndikti_knowledge?: string
  sndikti_specificskill?: string
}

interface KKNIProperty {
  plo: string
  kkni_autoresp?: string
  kkni_knowledge?: string
  kkni_workskill?: string
}

interface PEOMapPLOProperty {
  peo: string
  peoLabel?: string
  plo: Array<{
    hasPLORel: string
    ploLabel: string
    clo?: CLOProperty[]
    course?: string
  }>
}

interface CurriculumStructureProperty {
  peo: string
  hasPLORel: string
  hasCLORel: string
  hasULORel: string
}

type QueryProperty =
  | PLOProperty
  | SNDiktiProperty
  | KKNIProperty
  | PEOMapPLOProperty
  | CurriculumStructureProperty

export interface QueryApiResponse {
  success: string
  properties: QueryProperty[]
}
