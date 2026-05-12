// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title Kiro Token
 * @dev Proof-of-Work mineable ERC20 token with fair launch mechanism
 * 
 * Features:
 * - Free mint (only gas cost)
 * - PoW mining with keccak256
 * - Dynamic difficulty adjustment
 * - Per-wallet cap for fair distribution
 * - Decay reward system
 */
contract KiroToken is ERC20, Ownable {
    // Constants
    uint256 public constant MAX_SUPPLY = 21_000_000 * 1e18;
    uint256 public constant BASE_MINT_AMOUNT = 1000 * 1e18;
    uint256 public constant WALLET_CAP = 10_000 * 1e18;
    
    // State
    uint256 public totalMinted;
    uint256 public currentPowStage;
    
    // Mappings
    mapping(address => uint256) public mintedByAddress;
    mapping(address => bytes32) public currentPowChallenge;
    mapping(address => uint256) public lastMintBlock;
    
    // PoW difficulty stages (hex zeros → bits)
    // Stage 0: 6 hex zeros = 24 bits
    // Stage 1: 7 hex zeros = 28 bits
    // Stage 2: 8 hex zeros = 32 bits
    // Stage 3: 9 hex zeros = 36 bits
    // Stage 4: 10 hex zeros = 40 bits
    uint256[] public difficultyStages = [6, 7, 8, 9, 10];
    
    // Supply thresholds for difficulty increase
    uint256[] public supplyThresholds = [
        5_000_000 * 1e18,   // 5M → Stage 1
        10_000_000 * 1e18,  // 10M → Stage 2
        15_000_000 * 1e18,  // 15M → Stage 3
        18_000_000 * 1e18,  // 18M → Stage 4
        MAX_SUPPLY          // 21M → Max
    ];
    
    // Events
    event Minted(address indexed miner, uint256 amount, uint256 nonce, uint256 difficulty);
    event DifficultyIncreased(uint256 newStage, uint256 hexZeros, uint256 bits);
    event ChallengeGenerated(address indexed user, bytes32 challenge);
    
    constructor() ERC20("Kiro Token", "KIRO") Ownable(msg.sender) {
        // Contract starts with no pre-mine
        // All tokens must be mined via PoW
    }
    
    /**
     * @dev Get current PoW difficulty in hex zeros
     */
    function currentPowHexZeros() public view returns (uint256) {
        return difficultyStages[currentPowStage];
    }
    
    /**
     * @dev Get current PoW target (max hash value to be valid)
     */
    function POW_TARGET() public view returns (uint256) {
        uint256 hexZeros = currentPowHexZeros();
        return type(uint256).max >> (hexZeros * 4);
    }
    
    /**
     * @dev Get current PoW difficulty in bits
     */
    function POW_DIFFICULTY_BITS() public view returns (uint256) {
        return currentPowHexZeros() * 4;
    }
    
    /**
     * @dev Calculate actual mint amount with decay
     */
    function calculateActualMint(uint256 requested) public view returns (uint256) {
        if (totalMinted >= MAX_SUPPLY) return 0;
        
        uint256 remaining = MAX_SUPPLY - totalMinted;
        uint256 amount = requested;
        
        // Decay: reduce by 1% per 1M minted
        uint256 millionsMinted = totalMinted / (1_000_000 * 1e18);
        if (millionsMinted > 0) {
            uint256 decayPercent = millionsMinted;
            if (decayPercent > 90) decayPercent = 90; // Max 90% decay
            amount = amount * (100 - decayPercent) / 100;
        }
        
        // Cap at remaining supply
        if (amount > remaining) amount = remaining;
        
        // Minimum 1 token
        if (amount < 1e18 && remaining >= 1e18) amount = 1e18;
        
        return amount;
    }
    
    /**
     * @dev Generate new PoW challenge for user
     */
    function _generateChallenge(address user) internal {
        currentPowChallenge[user] = keccak256(
            abi.encodePacked(
                block.timestamp,
                block.prevrandao,
                user,
                totalMinted,
                lastMintBlock[user],
                blockhash(block.number - 1)
            )
        );
        emit ChallengeGenerated(user, currentPowChallenge[user]);
    }
    
    /**
     * @dev Check if PoW nonce is valid
     */
    function isValidPow(address user, uint256 powNonce) public view returns (bool) {
        bytes32 challenge = currentPowChallenge[user];
        if (challenge == bytes32(0)) return false;
        
        bytes32 hash = keccak256(abi.encodePacked(challenge, powNonce));
        return uint256(hash) <= POW_TARGET();
    }
    
    /**
     * @dev Initialize challenge for new user
     */
    function initChallenge() external {
        require(currentPowChallenge[msg.sender] == bytes32(0), "Challenge already exists");
        _generateChallenge(msg.sender);
    }
    
    /**
     * @dev Mine tokens with PoW
     * @param powNonce The nonce that solves the PoW challenge
     */
    function freeMint(uint256 powNonce) external {
        require(totalMinted < MAX_SUPPLY, "Max supply reached");
        require(mintedByAddress[msg.sender] < WALLET_CAP, "Wallet cap reached");
        require(currentPowChallenge[msg.sender] != bytes32(0), "No challenge, call initChallenge first");
        require(isValidPow(msg.sender, powNonce), "Invalid PoW solution");
        
        uint256 amount = calculateActualMint(BASE_MINT_AMOUNT);
        require(amount > 0, "Nothing to mint");
        
        // Check if need to increase difficulty
        if (currentPowStage < difficultyStages.length - 1) {
            if (totalMinted + amount >= supplyThresholds[currentPowStage]) {
                currentPowStage++;
                emit DifficultyIncreased(
                    currentPowStage,
                    currentPowHexZeros(),
                    POW_DIFFICULTY_BITS()
                );
            }
        }
        
        // Mint tokens
        _mint(msg.sender, amount);
        totalMinted += amount;
        mintedByAddress[msg.sender] += amount;
        lastMintBlock[msg.sender] = block.number;
        
        // Generate new challenge for next mint
        _generateChallenge(msg.sender);
        
        emit Minted(msg.sender, amount, powNonce, POW_DIFFICULTY_BITS());
    }
    
    /**
     * @dev Get comprehensive info about current state
     */
    function getInfo() external view returns (
        uint256 currentMinted,
        uint256 remainingSupply,
        uint256 currentDifficulty,
        uint256 nextMintAmount,
        uint256 stage
    ) {
        currentMinted = totalMinted;
        remainingSupply = MAX_SUPPLY - totalMinted;
        currentDifficulty = POW_DIFFICULTY_BITS();
        nextMintAmount = calculateActualMint(BASE_MINT_AMOUNT);
        stage = currentPowStage;
    }
    
    /**
     * @dev Get user-specific info
     */
    function getUserInfo(address user) external view returns (
        uint256 minted,
        uint256 balance,
        uint256 remainingCap,
        bytes32 challenge,
        bool hasChallenge
    ) {
        minted = mintedByAddress[user];
        balance = balanceOf(user);
        remainingCap = minted >= WALLET_CAP ? 0 : WALLET_CAP - minted;
        challenge = currentPowChallenge[user];
        hasChallenge = challenge != bytes32(0);
    }
}
