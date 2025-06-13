import { Flex, Text, Image, useBreakpointValue } from "@chakra-ui/react"
import { Link } from "@tanstack/react-router"

// import Logo from "/assets/images/fastapi-logo.svg"
import Logo from "/assets/images/Seagull-by-Rones.svg"
import UserMenu from "./UserMenu"

function Navbar() {
  const display = useBreakpointValue({ base: "none", md: "flex" })

  return (
    <Flex
      display={display}
      justify="space-between"
      position="sticky"
      color="white"
      align="center"
      bg="bg.muted"
      w="100%"
      top={0}
      p={4}
    >
      <Link to="/">
        <Flex align="center" gap={3}>
          {/*<Image src={Logo} alt="Logo" maxW="3xs" p={2} />*/}
          <Image src={Logo} alt="Logo" h="54.39px" objectFit="contain" />
          <Text fontSize="xl" fontWeight="bold" color="#aaccff">
            Medi-Verse
          </Text>
        </Flex>
      </Link>
      <Flex gap={2} alignItems="center">
        <UserMenu />
      </Flex>
    </Flex>
  )
}

export default Navbar
