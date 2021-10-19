// SPDX-License-Identifier: MIT

pragma solidity >=0.6.6 <0.9.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";


contract FundMe {
    
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;
    
    // constructor gets called the moment your smart contract is deployed
    constructor() public {
        owner = msg.sender;
    }
    
    function fund() public payable {
        // when you define a function as payable, you are telling the user that this function can be used for payments (ETH)
        // msg.sender & msg.value are keywords that can be used in any contract transaction.
        
        uint256 minimumUSD = 50 * 10 ** 18;
        require(getConversionRate(msg.value) >= minimumUSD, "You need to spend more ETH!");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
        
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
        return uint256(answer * 10000000000);
    }
    
    function getConversionRate(uint256  _ethAmount) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * _ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }
    
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    
    
    function withdraw() payable onlyOwner public {
        msg.sender.transfer(address(this).balance);
        for (uint256 funderIndex=0; funderIndex<funders.length; funderIndex++){
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
        
    }
}



