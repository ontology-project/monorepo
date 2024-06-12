import React from 'react'
import { Button, Flex, Link, Text } from '@chakra-ui/react'

interface NavBarProps {
  username: string
  isKaprodi: boolean
  logout: any
}

const NavBar: React.FC<NavBarProps> = ({ username, isKaprodi, logout }) => {
  const userRole = isKaprodi ? 'Kaprodi' : 'Reviewer'

  return (
    <Flex
      bg="purple.500"
      color="white"
      padding="4"
      justifyContent="space-between"
      alignItems="center"
    >
      <Text fontSize="lg" fontWeight="bold">
        Outcome Based Curriculum Ontology Project
      </Text>
      <Flex alignItems="center">
        {!isKaprodi && (
          <Link marginRight="8" href="/graphdb/query">
            Query
          </Link>
        )}
        {isKaprodi && (
          <Link marginRight="8" href="/graphdb/upload-excel">
            Upload Excel
          </Link>
        )}
        {isKaprodi && (
          <Link marginRight="8" href="/graphdb/kaprodi-reviews">
            Review
          </Link>
        )}
        <Text marginRight="8">
          Welcome, {username}! ({userRole})
        </Text>
        <Button onClick={logout}>Logout</Button>
      </Flex>
    </Flex>
  )
}

export default NavBar
