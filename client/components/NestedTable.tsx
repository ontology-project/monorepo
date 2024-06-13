import React from 'react'
import {
  Box,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
} from '@chakra-ui/react'
import { keyMappings, valueMappings } from '../utils/keyMappings'

interface NestedTableProps {
  data: any[]
  query: string
}

const NestedTable: React.FC<NestedTableProps> = ({ data, query }) => {
  const getDisplayKey = (key: string) => keyMappings[key] || key

  const getDisplayValue = (value: string) => valueMappings[value] || value

  const renderPLOTable = (ploArray: any[]) => (
    <Table size="sm">
      <Thead>
        <Tr>
          <Th>{getDisplayKey('hasPLORel')}</Th>
          {query !== 'Curriculum Structure' && (
            <Th>{getDisplayKey('ploLabel')}</Th>
          )}
          {query === 'CLO to Course Mapping' && (
            <Th>{getDisplayKey('hasCLORel')}</Th>
          )}
          {query === 'CLO to Course Mapping' && (
            <Th>{getDisplayKey('cloLabel')}</Th>
          )}
          {query === 'CLO to Course Mapping' && (
            <Th>{getDisplayKey('hasCourse')}</Th>
          )}
          {query === 'PLO to Course Mapping' && (
            <Th>{getDisplayKey('hasCourse')}</Th>
          )}
          {query === 'Curriculum Structure' && (
            <>
              <Th>{getDisplayKey('hasCLORel')}</Th>
              <Th>{getDisplayKey('hasULORel')}</Th>
            </>
          )}
        </Tr>
      </Thead>
      <Tbody>
        {ploArray.map((plo, index) => (
          <Tr key={index}>
            <Td>{getDisplayValue(plo.hasPLORel)}</Td>
            {query !== 'Curriculum Structure' && (
              <Td>{getDisplayValue(plo.ploLabel)}</Td>
            )}
            {query === 'CLO to Course Mapping' &&
              plo.clo &&
              plo.clo.length > 0 && (
                <>
                  {plo.clo.map((clo, cloIndex) => (
                    <React.Fragment key={cloIndex}>
                      <Td>{getDisplayValue(clo.hasCLORel)}</Td>
                      <Td>{getDisplayValue(clo.cloLabel)}</Td>
                      <Td>{getDisplayValue(clo.hasCourse)}</Td>
                    </React.Fragment>
                  ))}
                </>
              )}
            {query === 'PLO to Course Mapping' && (
              <Td>{getDisplayValue(plo.course)}</Td>
            )}
            {query === 'Curriculum Structure' && (
              <>
                <Td>{getDisplayValue(plo.hasCLORel)}</Td>
                <Td>{getDisplayValue(plo.hasULORel)}</Td>
              </>
            )}
          </Tr>
        ))}
      </Tbody>
    </Table>
  )

  return (
    <Box overflowX="auto">
      <Accordion allowMultiple>
        {data.map((item, index) => (
          <AccordionItem key={index}>
            <AccordionButton>
              <Box flex="1" textAlign="left" isTruncated>
                {item.peo}
                {query !== 'Curriculum Structure' && ` - ${item.peoLabel}`}
              </Box>
              {item.plo && item.plo.length > 0 && <AccordionIcon />}
            </AccordionButton>
            <AccordionPanel pb={4}>{renderPLOTable(item.plo)}</AccordionPanel>
          </AccordionItem>
        ))}
      </Accordion>
    </Box>
  )
}

export default NestedTable
