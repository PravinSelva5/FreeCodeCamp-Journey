// SPDX-License-Identifier: MIT

pragma solidity >=0.6.6 <0.9.0;

import "@chainlink/contracts/src/v0.8/interafaces/AggregatorV3Interface.sol";

contract FundMe {
    
    mapping(address => uint256) public addressToAmountFunded;
    
    function fund() public payable {
        // when you define a function as payable, you are telling the user that this function can be used for payments (ETH)
        // msg.sender & msg.value are keywords that can be used in any contract transaction.
        addressToAmountFunded[msg.sender] += msg.value;
        
        // what is the ETH -> USD conversion rate is?
        // This is where a oracle is needed to get off-chain data. The oracle is also responsible for validating it.
        // Remember interfaces don't have full function implementations
        // Solidity doesn't know how to interact with a contract natively, as a developer, we need to state which functions can be called.
        // Interfaces compile down to an ABI, tells solidity and other programming languages how it can interact with another contract.
        //  - Therefore, when trying to interact with another smart contract, you will need its ABI.
    }
        
    function getVersion() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331); 
        return priceFeed.version();
    }
    
    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
        // A tuple is a list of objects of potentially different types whose number is a constant at compile-time.
        
        (,int256 answer,,,) = priceFeed.latestRoundData();
        return uint256(answer * 1000000000);
    }
}