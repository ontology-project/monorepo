import React from 'react';
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
} from '@chakra-ui/react';
import { keyMappings, valueMappings } from '../utils/keyMappings';

interface NestedTableProps {
  data: any[];
  query: string;
}

const NestedTable: React.FC<NestedTableProps> = ({ data, query }) => {
  const getDisplayKey = (key: string) => keyMappings[key] || key;

  const getDisplayValue = (value: string) => valueMappings[value] || value;

  const renderPLOTable = (ploArray: any[]) => (
    <Table size="sm">
      <Thead>
        <Tr>
          <Th>{getDisplayKey('hasPLORel')}</Th>
          <Th>{getDisplayKey('ploLabel')}</Th>
          {query === "CLO to Course Mapping" && <Th>{getDisplayKey('hasCLORel')}</Th>}
          {query === "CLO to Course Mapping" && <Th>{getDisplayKey('cloLabel')}</Th>}
          {query === "CLO to Course Mapping" && <Th>{getDisplayKey('hasCourse')}</Th>}
          {query === "PLO to Course Mapping" && <Th>{getDisplayKey('hasCourse')}</Th>}
        </Tr>
      </Thead>
      <Tbody>
        {ploArray.map((plo, index) => (
          <Tr key={index}>
            <Td>{plo.hasPLORel}</Td>
            <Td>{plo.ploLabel}</Td>
            {query === "CLO to Course Mapping" && plo.clo && plo.clo.length > 0 && (
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
            {query === "PLO to Course Mapping" && <Td>{getDisplayValue(plo.course)}</Td>}
          </Tr>
        ))}
      </Tbody>
    </Table>
  );

  const renderPLO = (ploArray: any[]) => (
    <Accordion allowMultiple>
      {ploArray.map((plo, index) => (
        <AccordionItem key={index}>
          <AccordionButton>
            <Box flex="1" textAlign="left" isTruncated>
              {plo.hasPLORel} - {plo.ploLabel}
            </Box>
            {(query === "CLO to Course Mapping" && plo.clo && plo.clo.length > 0) && <AccordionIcon />}
          </AccordionButton>
          <AccordionPanel pb={4}>
            {query === "CLO to Course Mapping" && plo.clo && plo.clo.length > 0 ? (
              renderPLOTable([plo])
            ) : null}
          </AccordionPanel>
        </AccordionItem>
      ))}
    </Accordion>
  );

  return (
    <Box overflowX="auto">
      <Accordion allowMultiple>
        {data.map((item, index) => (
          <AccordionItem key={index}>
            <AccordionButton>
              <Box flex="1" textAlign="left" isTruncated>
                {item.peo} - {item.peoLabel}
              </Box>
              {item.plo && item.plo.length > 0 && <AccordionIcon />}
            </AccordionButton>
            <AccordionPanel pb={4}>
              {renderPLOTable(item.plo)}
            </AccordionPanel>
          </AccordionItem>
        ))}
      </Accordion>
    </Box>
  );
};

export default NestedTable;
