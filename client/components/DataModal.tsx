import React, { useEffect, useState } from 'react'
import {
  Text,
  Box,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalHeader,
  ModalOverlay,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Flex,
  ModalFooter,
  Button,
} from '@chakra-ui/react'
import { QueryApiResponse } from '../utils/types'
import { keyMappings, valueMappings } from '../utils/keyMappings'
import ReviewForm from './ReviewForm'
import NestedTable from './NestedTable'

interface DataModalProps {
  isOpen: boolean
  onClose: () => void
  data: QueryApiResponse | null
  query: string
  curriculum: string
}

const DataModal: React.FC<DataModalProps> = ({
  isOpen,
  onClose,
  data,
  query,
  curriculum,
}) => {
  const [currentPage, setCurrentPage] = useState(1)
  const rowsPerPage = 10

  useEffect(() => {
    if (!isOpen) {
      setCurrentPage(1)
    }
  }, [isOpen])

  const getDisplayKey = (key: string) => {
    return keyMappings[key] || key
  }

  const getDisplayValue = (value: string) => {
    return valueMappings[value] || value
  }

  const handleNextPage = () => {
    setCurrentPage((prev) => prev + 1)
  }

  const handlePreviousPage = () => {
    setCurrentPage((prev) => Math.max(prev - 1, 1))
  }

  const getPageData = () => {
    const startIndex = (currentPage - 1) * rowsPerPage
    const endIndex = startIndex + rowsPerPage
    return data?.properties.slice(startIndex, endIndex) || []
  }

  const renderTable = () => {
    if (
      query === 'PEO to PLO Mapping' ||
      query === 'PLO to Course Mapping' ||
      query === 'CLO to Course Mapping' ||
      query === 'Curriculum Structure'
    ) {
      return <NestedTable data={data?.properties} query={query} />
    }

    return (
      <Box overflowX="auto">
        <Table variant="simple">
          <Thead>
            <Tr>
              {data &&
                data.properties.length > 0 &&
                Object.keys(data.properties[0]).map((key) => (
                  <Th key={key}>{getDisplayKey(key)}</Th>
                ))}
            </Tr>
          </Thead>
          <Tbody>
            {getPageData().map((property, index) => (
              <Tr key={index}>
                {Object.entries(property).map(([key, value]) => (
                  <Td
                    key={key}
                    whiteSpace="normal"
                    overflow="hidden"
                    textOverflow="ellipsis"
                  >
                    {getDisplayValue(value)}
                  </Td>
                ))}
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>
    )
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="auto">
      <ModalOverlay />
      <ModalContent maxW="40vw">
        <ModalHeader>Query Results</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          {data && data.properties && data.properties.length > 0 ? (
            <>
              {renderTable()}
              <Flex justifyContent="space-between" my={4}>
                <Button
                  onClick={handlePreviousPage}
                  isDisabled={currentPage === 1}
                >
                  Previous
                </Button>
                <Text>
                  Page {currentPage} of{' '}
                  {Math.ceil(data.properties.length / rowsPerPage)}
                </Text>
                <Button
                  onClick={handleNextPage}
                  isDisabled={
                    currentPage ===
                    Math.ceil(data.properties.length / rowsPerPage)
                  }
                >
                  Next
                </Button>
              </Flex>
            </>
          ) : (
            <Text>No properties found.</Text>
          )}
        </ModalBody>
        <ModalFooter>
          <Flex w="full">
            <Box flex="1">
              <ReviewForm
                query={query}
                curriculum={curriculum}
                onSubmit={(review) => console.log(review)}
              />
            </Box>
          </Flex>
        </ModalFooter>
      </ModalContent>
    </Modal>
  )
}

export default DataModal
